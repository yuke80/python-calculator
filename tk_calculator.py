import tkinter as tk
import time

#create a constructor of class Calc inhrit from tk.Frame
class Calc(tk.Frame): 
    def __init__(self, master=None): #master frame
        super().__init__(master)
        
        self.bind("<Key>", self.key)
        self.focus_set()
        self.pack()
        
        #show input to user.
        self.frm_formula = tk.LabelFrame(self, text='Formula')
        self.frm_formula.pack(anchor='e')
        
        #show result to user.
        self.frm_result = tk.LabelFrame(self, text='Result')
        self.frm_result.pack(anchor='e')
        
        self.frm_func = tk.Frame(self)
        self.frm_func.pack(anchor='w')
        
        self.frm_button = tk.Frame(self)
        self.frm_button.pack(anchor='w')
        
        self.create_widgets()
        
    def create_widgets(self):
        self.result=tk.StringVar()
        self.result.set('0')
        self.formula=tk.StringVar()
        self.formula.set('')
        
        self.operand =""
        self.expr = ""
        self.clear_expr = False
        
        #formula ラベル(式表示)
        lb = tk.Label(self.frm_formula, textvariable=self.formula)
        lb.pack()
        #result ラベル(結果表示)
        lb = tk.Label(self.frm_result, textvariable=self.result)
        lb.pack()
 
        # create and bind clear button
        btn = tk.Button(self.frm_func,text='C',width=3)
        btn.bind("<Button-1>", self.clr_pushed)
        btn.grid(column=0, row=0)
 
        # create 1-9. buttons
        for n, cap in enumerate([7,8,9,4,5,6,1,2,3,0]):
            btn = tk.Button(self.frm_button,text=str(cap),width=3)
            btn.bind("<Button-1>", self.num_pushed)
            btn.grid(column=n%3, row=n//3)
        
        # create dot button    
        btn = tk.Button(self.frm_button,text='.',width=3)
        btn.bind("<Button-1>", self.dot_pushed)
        btn.grid(column=1, row=3)
 
        # create operater buttons
        for n, cap in enumerate(['/','*','-','+']):
            btn = tk.Button(self.frm_button, text=cap, width=3)
            btn.bind("<Button-1>", self.op_pushed)
            btn.grid(column=3, row=n)
 
        # create and bind equal button
        btn = tk.Button(self.frm_button,text='=',width=3)
        btn.bind("<Button-1>", self.eq_pushed)
        btn.grid(column=2, row=3)
 
    def num_pushed(self,event, kbd=None):
        """
        0-9. button pushed
        event.widget['txt']で押されたボタンの「数値」を取得して
        算術計算のオペランドを作成する。
        """
        if kbd is not None:
            num_str = kbd
        else:
            num_str=event.widget['text']
 
        self.clear_expr = False
            
        # 先頭が0以外の場合は追加
        if self.operand != "0":
            self.operand += num_str     
        # 0の場合は上書き
        else:
            self.operand = num_str
        self.result.set(self.operand)
        self.formula.set(self.expr + self.operand)
 
    def dot_pushed(self, event):
        """
        dot button pushed
        self.operand が空でない且つ、小数点を含んいなければ、小数点を追加する。
        """
        num_str = "."
        if self.operand == "":
            self.operand += "0" + num_str
        elif num_str not in self.operand:
            self.operand += num_str
        else:
            return
        self.result.set(self.operand)           
        self.formula.set(self.expr + self.operand)
 
    def op_pushed(self,event, kbd=None):
        '''
        operator(+ - / *) button pushed
        ボタンで入力されたオペランドをオペレータに適用して式を評価する。
        式の評価で例外が発生しなければ、self.exprに式を追加する。
        self.exprをformulaラベルに表示する。
        '''
        if kbd is not None:
            self.op = kbd
        else:
            self.op=event.widget['text']
            
        # Mar,23,'22 修正
        # 1+2=*3の入力で計算結果が9になるようにするため。
        if self.clear_expr:
            #self.expr = ""
            self.clear_expr = False
            self.operand = self.result.get()
 
        # try:
        #     # 式の最終オペランドは 暫定値"1"で評価する
        #     eval(self.expr + self.operand + self.op + "1")
        # except Exception as e:
        #     print(e)
        #     print(self.expr + self.operand + self.op + "1")
        # else:
        ex = self.expr + self.operand
        # 式が空
        if not ex:
            self.expr = "0" + self.op
        # 式の終端が演算子
        #elif ex[-1] in ["+", "-", "*", "/", "."]:
        elif not ex[-1].isnumeric():
            # 演算子を置換
            self.expr = ex[:-1] + self.op 
        else:    
            self.expr = self.expr + self.operand + self.op #this is easy to think.
        # result表示の "."を消去
        rst = self.result.get().rstrip(".")
        self.result.set(rst)
        # オペランドクリア
        self.operand = ""
        # 式の表示
        self.formula.set(self.expr)
 
    def eq_pushed(self,event):        
        '''
         equal(=) button pushed
        「=」ボタンが押されたらeval()で計算式を評価する。
        int型とfloat型を判定してresultラベルに表示する。
        self.expr をクリアする。
        '''
        try:
            ex = self.expr + self.operand
            print("ex=",ex)
            eval(ex)
        except SyntaxError as e:
            print(e)
            print("Error!", ex)
        except ZeroDivisionError:
            self.result.set("ZeroDivisionError")
            self.update()
            time.sleep(2)
            self.result.set("0")
            self.formula.set("")
            self.operand = ""
            self.exper = ""
        else:
            rslt = eval(ex)
            if isinstance(rslt,int):
                self.result.set("{:d}".format(rslt))
            # floatの場合 .is_integer()で小数点以下が"0"かの判定
            elif rslt.is_integer():
                self.result.set("{:d}".format(int(rslt)))
            else:
                self.result.set("{:f}".format(rslt).rstrip("0"))
            
            self.formula.set(ex + "=")
            self.expr=""
            self.operand = ""
            self.clear_expr = True
 
    def clr_pushed(self,event):
        '''
         clear(C) button pushed
        「C」ボタンが押されたら計算式と表示をクリアする
        '''
        self.expr = ""
        self.operand = ""
        self.result.set("0")
        self.formula.set("")
        
    def key(self,event):
        print( "pressed", repr(event.char))
        print("PRESSED", repr(event.keysym))
        if event.char in ["0","1","2","3","4",
                          "5","6","7","8","9"]:
            self.num_pushed(event, kbd=event.char)
            
        elif event.char == ".":
            self.dot_pushed(event)
 
        elif event.char in ["+", "-","*","/"]:
            self.op_pushed(event, kbd=event.char)
            
        elif event.char == "=" or event.char =="\r":
            self.eq_pushed(event)
            
        elif event.char.upper() == "C" :
            self.clr_pushed(event)
 
        #print(self.btn_dic[event.char].cget('relief'))
        #self.btn_dic[event.char].configure(relief = tk.SUNKEN)
        #self.update()
        #time.sleep(0.1)
        #self.btn_dic[event.char].configure(relief = tk.RAISED)
 
if __name__ == '__main__':
    root=tk.Tk()
    root.geometry('210x280+100+100')
    root.title("Cal")
    app = Calc(master=root)
    app.mainloop()
