import { makeAutoObservable, runInAction } from 'mobx';

export interface TreeItem {
  path: string;
  mode: string;
  type: 'blob' | 'tree' | 'commit';
  sha: string;
  size?: number;
  url: string;
}

export interface TreeResponse {
  sha: string;
  url: string;
  tree: TreeItem[];
  truncated: boolean;
}

export class TreeModel {
  owner: string;
  repo: string;
  sha: string;
  recursive = false;

  tree: TreeItem[] = [];
  truncated = false;
  loading = false;
  error: Error | null = null;

  constructor(owner: string, repo: string, sha: string) {
    this.owner = owner;
    this.repo = repo;
    this.sha = sha;
    makeAutoObservable(this);
  }

  async fetchTree(recursive = true): Promise<TreeResponse> {
    const url = `https://api.github.com/repos/${this.owner}/${this.repo}/git/trees/${this.sha}${
      recursive ? '?recursive=1' : ''
    }`;
    const res = await fetch(url, {
      headers: { Accept: 'application/vnd.github+json' },
    });
    if (!res.ok) throw new Error(`Failed to fetch tree: ${res.status}`);
    return (await res.json()) as TreeResponse;
  }

  async *openStream(): AsyncGenerator<TreeItem> {
    runInAction(() => {
      this.loading = true;
      this.error = null;
      this.tree = [];
      this.truncated = false;
    });

    try {
      // 1. 先递归查询，批量返回结果项
      const recursiveResult = await this.fetchTree(true);
      const seen = new Set<string>();

      for (const item of recursiveResult.tree) {
        if (!seen.has(item.sha + item.path)) {
          seen.add(item.sha + item.path);
          runInAction(() => this.tree.push(item));
          yield item;
        }
      }

      runInAction(() => {
        this.truncated = recursiveResult.truncated;
      });

      // 2. 若递归结果被截断，则依次非递归遍历已查询出的 tree 节点
      if (recursiveResult.truncated) {
        const queue: TreeItem[] = [...recursiveResult.tree.filter((i) => i.type === 'tree')];

        while (queue.length > 0) {
          const node = queue.shift()!;
          try {
            const sub = await this.fetchTree.call(
              { owner: this.owner, repo: this.repo, sha: node.sha, fetchTree: this.fetchTree },
              false,
            );
            for (const item of (sub as TreeResponse).tree) {
              const key = item.sha + item.path;
              if (!seen.has(key)) {
                seen.add(key);
                runInAction(() => this.tree.push(item));
                yield item;
              }
              if (item.type === 'tree') queue.push(item);
            }
          } catch (e) {
            runInAction(() => {
              this.error = e instanceof Error ? e : new Error(String(e));
            });
          }
        }
      }
    } catch (e) {
      runInAction(() => {
        this.error = e instanceof Error ? e : new Error(String(e));
      });
      throw e;
    } finally {
      runInAction(() => {
        this.loading = false;
      });
    }
  }
}