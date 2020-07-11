package command

import (
	"errors"
	"fmt"
	"strings"

	"github.com/spf13/cobra"
)

var (
	memberPeerURLs string
	isLearner      bool
)

// NewMemberCommand returns the cobra command for "member".
func NewMemberCommand() *cobra.Command {
	mc := &cobra.Command{
		Use:   "member <subcommand>",
		Short: "Membership related commands",
	}

	mc.AddCommand(NewMemberAddCommand())
	mc.AddCommand(NewMemberListCommand())

	return mc
}

// NewMemberAddCommand returns the cobra command for "member add".
func NewMemberAddCommand() *cobra.Command {
	cc := &cobra.Command{
		Use:   "add <memberName> [options]",
		Short: "Adds a member into the cluster",

		Run: memberAddCommandFunc,
	}

	cc.Flags().StringVar(&memberPeerURLs, "peer-urls", "", "comma separated peer URLs for the new member.")
	cc.Flags().BoolVar(&isLearner, "learner", false, "indicates if the new member is raft learner")

	return cc
}

// NewMemberListCommand returns the cobra command for "member list".
func NewMemberListCommand() *cobra.Command {
	cc := &cobra.Command{
		Use:   "list",
		Short: "Lists all members in the cluster",
		Long: `When --write-out is set to simple, this command prints out comma-separated member lists for each endpoint.
The items in the lists are ID, Status, Name, Peer Addrs, Client Addrs, Is Learner.
`,

		Run: memberListCommandFunc,
	}

	return cc
}

// memberAddCommandFunc executes the "member add" command.
func memberAddCommandFunc(cmd *cobra.Command, args []string) {
	if len(args) < 1 {
		ExitWithError(ExitBadArgs, errors.New("member name not provided"))
	}
	if len(args) > 1 {
		ev := "too many arguments"
		for _, s := range args {
			if strings.HasPrefix(strings.ToLower(s), "http") {
				ev += fmt.Sprintf(`, did you mean --peer-urls=%s`, s)
			}
		}
		ExitWithError(ExitBadArgs, errors.New(ev))
	}
	newMemberName := args[0]

	if len(memberPeerURLs) == 0 {
		ExitWithError(ExitBadArgs, errors.New("member peer urls not provided"))
	}

	urls := strings.Split(memberPeerURLs, ",")
	if isLearner {
		fmt.Printf("Learner, %v, %v\n", newMemberName, urls)
	} else {
		fmt.Printf("Not Learner, %v, %v\n", newMemberName, urls)
	}
}

// memberListCommandFunc executes the "member list" command.
func memberListCommandFunc(cmd *cobra.Command, args []string) {
    fmt.Printf("Display MemberList\n")
}
