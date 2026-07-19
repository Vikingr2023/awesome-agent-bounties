@@ -10,6 +10,7 @@
 import (
     "context"
     "errors"
+    "sync"
     "time"

     "github.com/go-redis/redis/v8/internal"
@@ -25,6 +26,7 @@
 type PubSub struct {
     client *Client

+    mu sync.Mutex
     channels map[string]*channel
     subscriptions map[string]*subscription
     receive chan *message
@@ -40,6 +42,7 @@
 func (ps *PubSub) ReceiveMessage(ctx context.Context) (*Message, error) {
     select {
     case msg, ok := <-ps.receive:
+        if !ok {
+            return nil, ctx.Err()
+        }
         if msg == nil {
             return nil, errors.New("pubsub: channel closed")
         }
@@ -50,6 +53,10 @@
         return &Message{
             Channel:  msg.channel,
             Pattern:  msg.pattern,
+            Payload:  msg.payload,
+            Err:      msg.err,
+        }, nil
+    case <-ctx.Done():
+        return nil, ctx.Err()
     }
 }

@@ -60,6 +67,12 @@
 func (ps *PubSub) reconnect(ctx context.Context) error {
     ps.mu.Lock()
     defer ps.mu.Unlock()

+    if err := ctx.Err(); err != nil {
+        return err
+    }
+
     // Close the current connection
     if ps.conn != nil {
         ps.conn.Close()
@@ -70,6 +83,10 @@
     // Re-subscribe to all channels and patterns
     for channel, _ := range ps.channels {
         if err := ps.subscribe(ctx, channel); err != nil {
+            if err := ctx.Err(); err != nil {
+                return err
+            }
+
             return err
         }
     }
@@ -80,6 +97,10 @@
     for pattern, _ := range ps.patterns {
         if err := ps.psubscribe(ctx, pattern); err != nil {
             if err := ctx.Err(); err != nil {
+                return err
+            }
+
+            return err
         }
     }

@@ -90,6 +111,10 @@
 func (ps *PubSub) subscribe(ctx context.Context, channel string) error {
     ps.mu.Lock()
     defer ps.mu.Unlock()
+
+    if err := ctx.Err(); err != nil {
+        return err
+    }
+
     if ps.conn == nil {
         return errors.New("pubsub: no connection")
     }
@@ -100,6 +125,10 @@
 func (ps *PubSub) psubscribe(ctx context.Context, pattern string) error {
     ps.mu.Lock()
     defer ps.mu.Unlock()
+
+    if err := ctx.Err(); err != nil {
+        return err
+    }
+
     if ps.conn == nil {
         return errors.New("pubsub: no connection")
     }
```

### Explanation:
1. **Immediate Return on Context Cancellation**: In `ReceiveMessage`, we check if the context is done and return `ctx.Err()` immediately.
2. **Reconnect Routine**: In the `reconnect` function, we check if the context is done before proceeding with the reconnection. This ensures that the reconnection does not continue if the context is cancelled.
3. **Subscribe and PSubscribe Functions**: In `subscribe` and `psubscribe`, we check if the context is done before proceeding. This prevents these functions from continuing if the context is cancelled.
4. **Mutex Locking**: The `mu` mutex is used to protect shared state, and we ensure it is not held indefinitely by checking the context before performing any operations.

This patch should resolve the concurrency issues and meet the acceptance criteria.