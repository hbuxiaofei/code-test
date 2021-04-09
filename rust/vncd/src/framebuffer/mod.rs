mod fb;

pub type FbFixScreeninfo = fb::fb_fix_screeninfo;
pub type FbVarScreeninfo = fb::fb_var_screeninfo;

pub const FBIOGET_VSCREENINFO: u32 = fb::FBIOGET_VSCREENINFO;
pub const FBIOGET_FSCREENINFO: u32 = fb::FBIOGET_FSCREENINFO;
