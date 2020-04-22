from MyQR import myqr
import os,qrcode,datetime
from tkinter import *
from tkinter import filedialog
import tkinter.messagebox
from PIL import Image

def selectPath():
    path_ = filedialog.askopenfilename()  # 选择文件 返回文件路径
    pic_path.set(path_)

def create_qrcode():
    # 获取各个输入框的值
    words = text.get(1.0,END)
    words = str(words)
    words = words.strip()
    picture = pic_path.get()
    picture = str(picture)
    radio = v.get()

    if words == '':
        tkinter.messagebox.showerror(title='error', message='填写二维码内容')         # 提出错误对话窗
        return False

    if radio == 2 and picture == '':
        tkinter.messagebox.showerror(title='error', message='个性二维码必须上传图片')         # 提出错误对话窗
        return False

    if picture != '':
        ex = picture.split('.')[-1] # 扩展名
        if not ex == 'jpg' and ex == 'jpeg' and ex == 'png' and ex == 'gif' :
            tkinter.messagebox.showerror(title='error', message='图片格式不符要求，要求为：jpg,gif,png,jpeg')         # 提出错误对话窗
            return False

    now = datetime.datetime.now()
    date_ = now.strftime('%Y-%m-%d %H%M%S')
    save_name = 'qrcode'+date_+'.png'
    if not os.path.exists(os.getcwd() + "/qrcode/"):
        os.mkdir(os.getcwd() + "/qrcode/")

    if radio == 1:
        qrcode_ (words,picture,save_name)
    elif radio == 2:
        myqr_ (words,picture,save_name)


def qrcode_ (words,picture,save_name):
    qr = qrcode.QRCode(
        version = 5,  # 设置容错率为最高
        error_correction = qrcode.ERROR_CORRECT_H,  # 用于控制二维码的错误纠正程度
        box_size = 10,  # 控制二维码中每个格子的像素数，默认为10
        border = 1,  # 二维码四周留白，包含的格子数，默认为4
    )

    qr.add_data(words)  # QRCode.add_data(data)函数添加数据
    qr.make(fit=True)  # QRCode.make(fit=True)函数生成图片

    img = qr.make_image()
    img = img.convert("RGBA")  # 二维码设为彩色
    if picture != '':
        logo = Image.open(picture)  # 传gif生成的二维码也是没有动态效果的
        w,h = img.size  # 二维码大小
        logo_w = int(w/4)  # 二维码中间logo 大小
        logo_h = int(h/4)
        logo = logo.resize((logo_w, logo_h)) # 重设logo图片对象大小
        l_w = int((w - logo_w) / 2)
        l_h = int((h - logo_h) / 2)  # logo 在二维码中位置
        logo = logo.convert("RGBA")
        img.paste(logo, (l_w, l_h), logo)  # 把logo粘贴到二维码中
    img.save(os.getcwd() + "/qrcode/" + save_name, quality=100)
    img.show()

def myqr_ (words,picture,save_name):
    match_obj = re.match("[\u4E00-\u9FA5]+", words)
    if match_obj:
        tkinter.messagebox.showerror(title='error', message='个性二维码暂不支持中文')         # 提出错误对话窗
        return False

    ex = picture.split('.')[-1] # 扩展名
    if ex == 'gif':
        save_name = save_name.split('.')[0]+'.'+ex
    myqr.run(
        words = words,  # 可以是字符串，也可以是网址(前面要加http(s)://)
        version = 5,  # 设置容错率为最高
        level = 'H',  # 控制纠错水平，范围是L、M、Q、H，从左到右依次升高
        picture = picture,  # 将二维码和图片合成
        colorized = True,  # 彩色二维码
        contrast = 1.0,  # 用以调节图片的对比度，1.0 表示原始图片，更小的值表示更低对比度，更大反之。默认为1.0
        brightness = 1.0,  # 用来调节图片的亮度，其余用法和取值同上
        save_name = save_name,  # 保存文件的名字，格式可以是jpg,png,bmp,gif
        save_dir = os.getcwd()+'/qrcode'  # 控制位置
    )
    Image.open(os.getcwd()+'/qrcode/'+save_name).show()



if __name__=="__main__":
    frame = Tk()
    frame.title('生成二维码')

    label_name = Label(frame,text = "填写二维码内容:").grid(row = 0,column = 0)
    label_age = Label(frame,text = "选择二维码中的图片:",height='2').grid(row = 2,column = 0)

    text = Text(frame,width = 80,height=8)
    text.grid(row = 0,column = 1)

    pic_path = StringVar()
    # 绑定变量path
    path = Label(frame, textvariable = pic_path,width = 80)
    path.grid(row = 2, column = 1)

    btn = Button(frame, text = "选择图片", command = selectPath)
    btn.grid(row = 2, column = 1)
    btn.place(x=130, y=113)

    v = IntVar() # 定义单选框值
    v.set(1) # 默认值
    radio1 = Radiobutton(frame,text="普通二维码",variable=v,value=1)  # 绑定变量v
    radio1.grid(row = 3,column = 1)
    radio1.place(x=220, y=150)
    radio2 = Radiobutton(frame,text="个性二维码(支持gif动态)",variable=v,value=2)
    radio2.grid(row = 3,column = 1)
    radio2.place(x=380, y=150)

    button_ok = Button(frame,text = "确定",width = 10,height = "1",command=create_qrcode)
    button_ok.grid(row = 4,column = 0)
    button_ok.place(x=220, y=190)
    button_cancel = Button(frame,text = "取消",width = 10,height = "1",command=frame.quit)
    button_cancel.grid(row = 4,column = 1)
    button_cancel.place(x=380, y=190)

    Label(frame,text = "",height = "4").grid(row = 5,column = 0)

    frame.mainloop()



