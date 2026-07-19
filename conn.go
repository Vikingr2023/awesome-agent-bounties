import (
    "net"
    "sync/atomic"
)

type Conn struct {
    // Other fields...
    closeChan chan struct{}
    closing   uint32 // 0: not closing, 1: closing
}

func (c *Conn) Close() error {
    if!atomic.CompareAndSwapUint32(&c.closing, 0, 1) {
        return nil // Already closing
    }

    // Close the underlying network connection
    c.conn.Close()

    // Signal all goroutines to exit
    close(c.closeChan)

    return nil
}

func (c *Conn) WriteMessage(messageType int, data []byte) error {
    select {
    case <-c.closeChan:
        return net.ErrClosed
    default:
    }

    // Existing write message logic
    //...

    return nil
}

func (c *Conn) WriteControl(messageType int, data []byte, deadline time.Time) error {
    select {
    case <-c.closeChan:
        return net.ErrClosed
    default:
    }

    // Existing write control logic
    //...

    return nil
}

func (c *Conn) NextWriter(messageType int) (io.WriteCloser, error) {
    select {
    case <-c.closeChan:
        return nil, net.ErrClosed
    default:
    }

    // Existing next writer logic
    //...

    return nil, nil
}