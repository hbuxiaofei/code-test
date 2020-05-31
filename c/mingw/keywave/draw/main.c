#include <windows.h>
#include <stdbool.h>
#include <stdio.h>
#include <signal.h>
#include <dbt.h>
#include <tchar.h>
#include <time.h>


#ifndef MAX_PATH
#define MAX_PATH 128
#endif

#ifndef MAX_STRING
#define MAX_STRING 1024
#endif


static char *g_module_dir = NULL;


LPCWSTR str2lpcwstr(const char* str, WCHAR* wsz)
{
    memset(wsz, 0, sizeof(wsz));
    MultiByteToWideChar(CP_ACP, 0, str, strlen(str)+1, wsz,
            sizeof(wsz)/sizeof(wsz[0]));
    return (LPCWSTR)wsz;
}


char* lpcwstr2str(WCHAR* lpcwszStr, char* str)
{
    memset(str, 0, sizeof(str));
    DWORD dwMinSize = 0;

    dwMinSize = WideCharToMultiByte(CP_OEMCP, 0, lpcwszStr, -1, NULL, 0, NULL, false);
    if (0 == dwMinSize) {
        return str;
    }
    WideCharToMultiByte(CP_OEMCP, 0, lpcwszStr, -1, str, dwMinSize, NULL, false);
    return str;
}


// check if directory exist
bool is_dir_exist(const char* dir)
{
	WIN32_FIND_DATA find_data;
	bool val= false;
	HANDLE h_find = FindFirstFile(dir, &find_data);
    if ((h_find != INVALID_HANDLE_VALUE) &&
            (find_data.dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY)) {
        val= true;
    }
	FindClose(h_find);
	return val;
}


void logging(const char *format,...)
{
    return;
}


void show_file(HDC hdc, char *file)
{
    FILE *fp = NULL;
    wchar_t wsz_buf[MAX_STRING] = {0};
    wchar_t *wsz_end = L"# Analysis";
    int wsz_len = 0;
    int row = 50;
    int col = 900;

    logging("Open file: %s\n", file);

    fp = fopen(file, "r,ccs=UTF-8");
    if (fp != NULL) {
        while(fgetws(wsz_buf, sizeof(wsz_buf) - sizeof(wchar_t), fp) != NULL ) {
            if (wcsncmp(wsz_buf, wsz_end, wcslen(wsz_end)) == 0) {
                break;
            }
            wsz_len = wcslen(wsz_buf);
            if (wsz_len >= 2) {
                wsz_len -= 1;
            } else {
                wsz_len = 0;
            }

            TextOutW(hdc, col, row, wsz_buf, wsz_len);
            row += 20;
            memset(wsz_buf, 0, sizeof(wsz_buf));
        }
        fclose(fp);
    } else {
        logging("Open file(%s) error!\n", file);
    }
}


HFONT create_format_font(LPCTSTR face, int width, int height, int angle)
{
	HFONT hFont;
	hFont = CreateFont(
			height,      //字体的逻辑高度
			width,       //逻辑平均字符宽度
			angle,       //与水平线的角度
			0,           //基线方位角度
			FW_REGULAR,  //字形：常规
			FALSE,       //字形：斜体
			FALSE,       //字形：下划线
			FALSE,       //字形：粗体
			GB2312_CHARSET,          //字符集
			OUT_DEFAULT_PRECIS,      //输出精度
			CLIP_DEFAULT_PRECIS,     //剪截精度
			PROOF_QUALITY,           //输出品质
			FIXED_PITCH | FF_MODERN, //倾斜度
			face                     //字体
			);
	return hFont;
}


void draw_text_from_file(char *file)
{
    // 获取一个可供画图的DC
    HDC hdc = GetWindowDC(GetDesktopWindow());
    /* HDC hdc = GetWindowDC(HWND_DESKTOP); */
    if (hdc == NULL) {
        logging("Get HDC error!\n");
    } else {
        logging("Get HDC: %ld   %d\n", hdc, GetDesktopWindow());
    }

	// 创建红色1像素宽度的实线画笔
	HPEN hpen1 = CreatePen(PS_SOLID, 8, RGB(255, 0, 0));
	// 创建一个实体蓝色画刷
	HBRUSH hbrush1 = CreateSolidBrush(RGB(0, 0, 255));
	// 创建字体
	HFONT hfont1 = create_format_font((LPCTSTR)"宋体", 0, 15, 0);

	// 将hpen1和hbrush1选进HDC，并保存HDC原来的画笔和画刷
	HPEN hpen_old = (HPEN)SelectObject(hdc, hpen1);
	HBRUSH hbrush_old = (HBRUSH)SelectObject(hdc, hbrush1);
	HFONT hfont_old = (HFONT)SelectObject(hdc, hfont1);

    show_file(hdc, file);

	// 恢复原来的画笔和画刷
	SelectObject(hdc, hpen_old);
	SelectObject(hdc, hbrush_old);
	SelectObject(hdc, hfont_old);
}


void do_wall_text(void *args)
{
    char text_file[MAX_PATH] = {0};
    strcpy(text_file, g_module_dir);
    strcat(text_file, "\\text\\");

    WIN32_FIND_DATA *p_find_data = (WIN32_FIND_DATA *)args;
    if (p_find_data && p_find_data->cFileName) {

        strcat(text_file, p_find_data->cFileName);

        draw_text_from_file(text_file);

    } else {
        Sleep(1);
    }
}


void for_each_files(const char* dir, void (*pf)(void *))
{
    HANDLE f_find;
    WIN32_FIND_DATA find_data;
    char buf[MAX_PATH] = {0};

    if (!is_dir_exist(dir)) {
        return;
    }

    strcpy(buf, dir);
    strcat(buf, "\\*.*");

	f_find = FindFirstFile(buf, &find_data);
    if (f_find == INVALID_HANDLE_VALUE) {
        logging("Find first file error\n");
        return;
    }
	do {
		// ignore "." and ".."
        if (strcmp(find_data.cFileName, ".") == 0 ||
                strcmp(find_data.cFileName, "..") == 0)
            continue;

        // not directory
        if (!(find_data.dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY)) {
            logging("file name: %s\n", find_data.cFileName);
            if (pf)
                (*pf)((void *)&find_data);
		}
	} while (FindNextFile(f_find, &find_data));
	FindClose(f_find);
}


static int draw_once(void)
{
    char text_dir[MAX_PATH] = {0};

    strcpy(text_dir, g_module_dir);
    strcat(text_dir, "\\text");

    logging("Start run agent once...\n");

    for_each_files(text_dir, do_wall_text);

    return EXIT_SUCCESS;
}


void draw_window()
{
    // 获取一个可供画图的DC，我这里就直接用桌面算了
    HDC hdc = GetWindowDC(GetDesktopWindow());

    // 创建红色1像素宽度的实线画笔
    HPEN hpen1 = CreatePen(PS_SOLID, 1, RGB(255, 0, 0));
    // 创建一个实体蓝色画刷
    HBRUSH hbrush1 = CreateSolidBrush(RGB(0, 0, 255));

    // 创建绿色5像素宽度的破折画笔
    HPEN hpen2 = CreatePen(PS_DASH, 5, RGB(0, 255, 0));
    // 创造一个透明的画刷
    HBRUSH hbrush2 = (HBRUSH)GetStockObject(NULL_BRUSH);

    // 将hpen1和hbrush1选进HDC，并保存HDC原来的画笔和画刷
    HPEN hpen_old = (HPEN)SelectObject(hdc, hpen1);
    HBRUSH hbrush_old = (HBRUSH)SelectObject(hdc, hbrush1);

    // 在(40,30)处画一个宽50像素，高50像素的矩形
    Rectangle(hdc, 40, 30, 40 + 50, 30 + 50);


    // 换hpen2和hbrush2
    SelectObject(hdc, hpen2);
    SelectObject(hdc, hbrush2);

    // 在(40,100)处画一个矩形
    Rectangle(hdc, 40, 100, 40 + 200, 100 + 50);

    // 画个椭圆看看
    Ellipse(hdc, 40, 200, 40 + 200, 200 + 80);

    // 画个(0,600)到(800,0)的直线看看
    MoveToEx(hdc, 0, 600, NULL);
    LineTo(hdc, 800, 0);

    // 在(700,500)处画个黄点，不过这个点只有一像素大小，你细细的看才能找到
    SetPixel(hdc, 700, 500, RGB(255, 255, 0));

    //文字 参数：桌面句柄，XY坐标，文字，文字宽度
    TextOutA(hdc, 700, 500, "Hello, World!", 13);

    wchar_t text1[] = L"你好";
    TextOutW(hdc, 800, 500, text1, wcslen(text1));

    // 恢复原来的画笔和画刷
    SelectObject(hdc, hpen_old);
    SelectObject(hdc, hbrush_old);
}

HFONT CreateFormatFont(LPCTSTR face, int width, int height, int angle)
{
	HFONT hFont;
	hFont = CreateFont(
			height,      //字体的逻辑高度
			width,       //逻辑平均字符宽度
			angle,       //与水平线的角度
			0,           //基线方位角度
			FW_REGULAR,  //字形：常规
			FALSE,       //字形：斜体
			FALSE,       //字形：下划线
			FALSE,       //字形：粗体
			GB2312_CHARSET,          //字符集
			OUT_DEFAULT_PRECIS,      //输出精度
			CLIP_DEFAULT_PRECIS,     //剪截精度
			PROOF_QUALITY,           //输出品质
			FIXED_PITCH | FF_MODERN, //倾斜度
			face                     //字体
			);
	return hFont;
}

void draw_text()
{
    wchar_t text1[] = L"你好，这是一个测试，恭喜你！";

    // 获取一个可供画图的DC，我这里就直接用桌面算了
    HDC hdc = GetWindowDC(GetDesktopWindow());

    // 创建红色1像素宽度的实线画笔
    HPEN hpen1 = CreatePen(PS_SOLID, 8, RGB(255, 0, 0));
    // 创建一个实体蓝色画刷
    HBRUSH hbrush1 = CreateSolidBrush(RGB(0, 0, 255));
    // 创建字体
    HFONT hfont1 = CreateFormatFont((LPCTSTR)"黑体", 0, 20, 0);

    // 将hpen1和hbrush1选进HDC，并保存HDC原来的画笔和画刷
    HPEN hpen_old = (HPEN)SelectObject(hdc, hpen1);
    HBRUSH hbrush_old = (HBRUSH)SelectObject(hdc, hbrush1);
    HFONT hfont_old = (HFONT)SelectObject(hdc, hfont1);

    TextOutW(hdc, 900, 20, text1, wcslen(text1));

    // 恢复原来的画笔和画刷
    SelectObject(hdc, hpen_old);
    SelectObject(hdc, hbrush_old);
    SelectObject(hdc, hfont_old);
}


int main()
{
    static char module_dir[MAX_PATH] = {0};

    GetModuleFileName(NULL, module_dir, MAX_PATH);
    *strrchr(module_dir, '\\') = 0;
    g_module_dir = module_dir;

    /* draw_text(); */

    draw_once();
    return 0;
}
