package command


// GlobalFlags are flags that defined globally
// and are inherited to all sub-commands.
type GlobalFlags struct {
    Endpoints             []string
    OutputFormat string
    IsHex        bool

    User     string
    Password string

    Debug bool
}

