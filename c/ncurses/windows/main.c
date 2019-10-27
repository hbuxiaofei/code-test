#include <test.priv.h>
#include <time.h>

/*
 *  Trap interrupt
 */
static void trap(int sig GCC_UNUSED)
{
    exit_curses();
    ExitProgram(EXIT_FAILURE);
}

/*
 *  Wait for user
 */
static int WaitForUser(WINDOW *win)
{
    time_t t;

    /* nodelay(win, TRUE); */
    t = time((time_t *) 0);

    while (1) {
        chtype key;
        if ((int) (key = (chtype) wgetch(win)) != ERR) {
            if (key == 'q' || key == 'Q')
                return 1;
            else
                return 0;
        }
        if (time((time_t *) 0) - t > 5) {
            return 0;
        }
    }
}

static void set_colors(WINDOW *win, int pair, int foreground, int background)
{
    if (has_colors()) {
        if (pair > COLOR_PAIRS)
            pair = COLOR_PAIRS;
        init_pair((short) pair, (short) foreground, (short) background);
        (void) wattrset(win, AttrArg(COLOR_PAIR(pair), 0));
    }
}

static chtype use_colors(WINDOW *win, int pair, chtype attrs)
{
    if (has_colors()) {
        if (pair > COLOR_PAIRS)
            pair = COLOR_PAIRS;
        attrs |= (chtype) COLOR_PAIR(pair);
    }
    (void) wattrset(win, AttrArg(attrs, 0));
    return attrs;
}

/*
 * Sub windows
 */
static int SubWinTest(WINDOW *win)
{
    int w, h, sw, sh, bx, by;
    WINDOW *swin1, *swin2, *swin3;
    static int index = 1;

    (void) h;
    getmaxyx(win, h, w);
    getbegyx(win, by, bx);
    sw = w / 3;
    sh = 3;

    if ((swin1 = subwin(win, sh, sw, by + 3, bx + 5)) == NULL) {
        return 1;
    }
    if ((swin2 = subwin(win, sh, sw, by + 6, bx + 8)) == NULL) {
        delwin(swin1);
        return 1;
    }
    if ((swin3 = subwin(win, sh, sw, by + 9, bx + 11)) == NULL) {
        delwin(swin1);
        delwin(swin2);
        return 1;
    }

    use_colors(swin1, 1, A_NORMAL);
    box(swin1, ' ', ' ');
    if (index == 1)
        set_colors(swin1, 8, COLOR_RED, COLOR_BLUE);
    else
        set_colors(swin1, 8, COLOR_RED, COLOR_BLACK);
    /* werase(swin1); */
    MvWAddStr(swin1, 1, 3, "Sub-window 1");
    wrefresh(swin1);

    use_colors(swin2, 1, A_NORMAL);
    box(swin2, ' ', ' ');
    if (index == 2)
        set_colors(swin2, 9, COLOR_CYAN, COLOR_MAGENTA);
    else
        set_colors(swin2, 9, COLOR_CYAN, COLOR_BLACK);
    /* werase(swin2); */
    MvWAddStr(swin2, 1, 3, "Sub-window 2");
    wrefresh(swin2);

    use_colors(swin3, 1, A_NORMAL);
    box(swin3, ' ', ' ');
    /* box(swin3, 0, 0); */
    if (index == 3)
        set_colors(swin3, 10, COLOR_YELLOW, COLOR_RED);
    else
        set_colors(swin3, 10, COLOR_YELLOW, COLOR_BLACK);
    /* werase(swin3); */
    MvWAddStr(swin3, 1, 3, "Sub-window 3");
    wrefresh(swin3);

    if (++index >  3)
        index = 1;

    delwin(swin1);
    delwin(swin2);
    delwin(swin3);
    return 0;
}


int main(int argc GCC_UNUSED, char *argv[]GCC_UNUSED)
{
    WINDOW *win;
    int width, height;
    int i, j;
    char *msg_quit = " Type 'q' or 'Q' to quit ";
    static int count = 1;

    setlocale(LC_ALL, "");

    InitAndCatch(initscr(), trap);
    if (has_colors())
        start_color();
    cbreak();
    curs_set(0);

    width = 70;
    height = 20;
    /* Create a drawing window */
    win = newwin(height, width, (LINES - height) / 2, (COLS - width) / 2);
    if (win == NULL) {
        exit_curses();
        ExitProgram(EXIT_FAILURE);
    }

    while (1) {
        werase(win);
        box(win, ACS_VLINE, ACS_HLINE);
        wrefresh(win);

        /* Erase and draw window */
        set_colors(win, 1, COLOR_YELLOW, COLOR_BLACK);
        wbkgd(win, use_colors(win, 1, A_BOLD));
        werase(win);
        wrefresh(win);

        /* Draw bounding box */
        set_colors(win, 2, COLOR_WHITE, COLOR_CYAN);
        box(win, ' ', ' ');
        MvWAddStr(win, 0, 2, ".config - Make Isoimage(aarch64) Configuration");
        wrefresh(win);

        /* Draw sub windows */
        SubWinTest(win);

        i = height - 2;
        j = (width - strlen(msg_quit)) / 2;
        set_colors(win, 3, COLOR_BLUE, COLOR_WHITE);
        MvWAddStr(win, i, j, msg_quit);
        wrefresh(win);

        set_colors(win, 4, COLOR_BLUE, COLOR_RED);
        switch (count) {
            case 1:
                MvWAddStr(win, height - 4, 2, "Show sub windows");
                count ++;
                break;
            case 2:
                MvWAddStr(win, height - 4, 2, "                        ");
                count ++;
                break;
            case 3:
                count ++;
                use_colors(win, 3, A_NORMAL);
                MvWAddStr(win, height - 4, 2, "Show sub windows");
                break;
            case 4:
                count ++;
                MvWAddStr(win, height - 4, 2, "                         ");
                break;
            default:
                break;
        }
        wrefresh(win);
        if (count > 4)
            count = 1;

        if (WaitForUser(win) == 1)
            break;
    }
    exit_curses();
    ExitProgram(EXIT_SUCCESS);
}
