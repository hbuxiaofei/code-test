#include <windows.h>
#include <stdbool.h>
#include <stdio.h>
#include <signal.h>
#include <dbt.h>
#include <tchar.h>
#include <time.h>

#pragma comment( linker, "/subsystem:\"windows\" /entry:\"mainCRTStartup\"" )

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
    Sleep(100);
    TextOutW(hdc, 900, 20, text1, wcslen(text1));
    Sleep(100);

    // 恢复原来的画笔和画刷
    SelectObject(hdc, hpen_old);
    SelectObject(hdc, hbrush_old);
    SelectObject(hdc, hfont_old);
}



int main()
{
    fclose(stdout);
    fclose(stderr);
    fclose(stdin);
    draw_text();
    return 0;
}
