import (
    "time"
)

type Node struct {
    // existing fields
    State          State
    IncarnationNum uint64
    LastUpdated    time.Time
}

type State int

const (
    StateUnknown State = iota
    StateAlive
    StateSuspect
    StateDead
    StateLeft
)

func (n *Node) TransitionTo(state State, incarnationNum uint64) {
    if n.State == StateDead && state!= StateAlive {
        // Prevent transitioning from Dead to Suspect or other states
        return
    }

    if state == StateSuspect && n.State == StateDead {
        // Only allow transition to Suspect if the incoming message has a higher incarnation number
        if incarnationNum <= n.IncarnationNum {
            return
        }
    }

    n.State = state
    n.IncarnationNum = incarnationNum
    n.LastUpdated = time.Now()
}

func (m *Membership) ProcessGossipMessage(msg *GossipMessage) {
    node, ok := m.nodeMap[msg.NodeID]
    if!ok {
        // Handle new node
        node = &Node{State: StateUnknown}
        m.nodeMap[msg.NodeID] = node
    }

    // Determine the new state based on the message
    var newState State
    switch msg.Type {
    case GossipTypeAlive:
        newState = StateAlive
    case GossipTypeSuspect:
        newState = StateSuspect
    case GossipTypeDead:
        newState = StateDead
    default:
        return
    }

    // Transition the node to the new state
    node.TransitionTo(newState, msg.IncarnationNum)
}

func (m *Membership) GarbageCollect() {
    now := time.Now()
    for nodeID, node := range m.nodeMap {
        if node.State == StateDead && now.Sub(node.LastUpdated) > m.TombstoneTimeout {
            delete(m.nodeMap, nodeID)
        }
    }
}