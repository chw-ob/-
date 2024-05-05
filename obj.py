from sympy import symbols, Eq, Matrix, solve
import sympy
import numpy as np
import math
import copy
from decimal import Decimal
import matplotlib
import matplotlib.pyplot as plt
  
class component():
    def __init__(self, net=[], property=None):
        self.net = net
        self.property = property

    def get_net(self):
        return self.net

    def get_property(self):
        return self.property

    def get_sti_n(self,A):
        return A

    def get_kind(self):
        return None

    def get_n(self, List):
        for i in self.net:
            List.add(i)
        return List

    def get_List_R(self,List):
        return List

    def get_List_S(self,List):
        return List

    def get_List_X(self,List):
        return List

    def get_matrix_A(self, A, i):
        A[self.net[0], i] = 1
        A[self.net[1], i] = -1
        return A

    def get_state_A2(self,List):
        List.append(1)
        return List


    def get_vector_Usb(self,Usb,i):
        return Usb

    def get_vector_Ub(self,Ub,i):
        return Ub
        pass

    def get_vector_Zb(self,Zb,i):
        return Zb
        pass

    def get_vector_Ib(self,Ib,i):
        return Ib
        pass

    def get_vector_Isb(self,Isb,i):
        return Isb
        pass

    def get_matrix_F(self,F,i):
        return F
        pass

    def get_matrix_H(self,H,i):
        return H
        pass

    def get_vector_Un(self,Un,i):
        return Un

    def get_complex_F(self,F,i,f):
        return self.get_matrix_F(F,i)

    def get_complex_H(self,H,i,f):
        return self.get_matrix_H(H,i)

    def get_state_variable(self,List):
        return List
class component_R(component):
    def get_kind(self):
        return "R"
    def get_vector_Zb(self, Zb, i):
        Zb[i, i] = self.property
        return Zb

    def get_matrix_F(self, F, i):
        F[i, i] = -1
        return F
    def get_matrix_H(self, H, i):
        H[i, i] = self.property
        return H
    def get_List_R(self,List):
        List.append(self)
        return List
class component_source_v(component):
    def get_kind(self):
        return "source_v"
    def get_vector_Usb(self, Usb, i):
        Usb[i, 0] = self.property
        return Usb
    def get_matrix_F(self, F, i):
        F[i, i] = 1
    def get_List_S(self,List):
        List.append(self)
        return List
    def get_state_A2(self,List):
        List.append(2)
        return List
    def get_sti_value(self,index):
        return self.property
class componnet_sin_source_v(component_source_v):
    def __init__(self,net,property):
        self.net=net
        self.property=property[0]
        self.F=property[1]
    def get_sti_value(self,t):
        return self.property*math.sin(t*self.F)
class componnet_fang_source_v(component_source_v):
    def __init__(self,net,property):
        self.net=net
        self.property=property[0]
        self.F=property[1]
    def get_sti_value(self,t):
        t = Decimal(str(t))
        T = Decimal(str(1 / self.F))
        t = t % T
        if t < T / 2:
            #print(self.property)
            return self.property
        else:
            #print(0)
            return 0
class component_Y(component):
    def get_kind(self):
        return "Y"
    def get_matrix_H(self,H,i):
        H[i,i]=-1
    def get_matrix_F(self,F,i):
        F[i,i]=self.property
    def get_List_R(self,List):
        List.append(self)
        return List
class component_source_i(component):
    def get_kind(self):
        return "source_i"
    def get_matrix_H(self,H,i):
        H[i,i]=1
    def get_vector_Isb(self,Isb,i):
        Isb[i,0]=self.property
    def get_List_S(self, List):
        List.append(self)
        return List
    def get_state_A2(self,List):
        List.append(3)
        return List
    def get_sti_value(self,index):
        return 1
class component_sin_source_i(component_source_i):
    def __init__(self,net,property):
        self.net=net
        self.property=property[0]
        self.F=property[1]
    def get_kind(self):
        return "sin_source_i"
    def get_sti_value(self,t):
        return self.property*math.sin(t*self.F)
class component_C(component):
    def get_complex_F(self,F,i,f):
        F[i,i]=f*self.property*sympy.I
        return F
    def get_complex_H(self,H,i,f):
        H[i,i]=-1
        pass
    def get_sti_n(self,A):
        return A+1
    def get_kind(self):
        return "C"
    def get_state_variable(self,List):
        List.append("C")
        return List
    def get_List_X(self,List):
        List.append(self)
        return List
    def get_state_A2(self,List):
        List.append(4)
        return List
    def get_init_value(self):
        return 0
class component_L(component):
    def get_complex_F(self,F,i,f):
        F[i,i]=-1
        return F
    def get_complex_H(self,H,i,f):
        H[i,i]=f*self.property*sympy.I
        return H
    def get_sti_n(self,A):
        return A+1
    def get_kind(self):
        return "L"
    def get_state_variable(self,List):
        List.append("l")
        return List
    def get_List_X(self,List):
        List.append(self)
        return List
    def get_state_A2(self, List):
        List.append(5)
        return List
    def get_init_value(self):
        return 0
class calculator():
    def __init__(self):
        pass

    @staticmethod
    def get_equal_complex_R(e_temp, net_1, net_2,f):
        import copy
        e = copy.deepcopy(e_temp)
        i = 0
        while i < len(e):
            if e[i].get_kind() == "source_v":
                if e[i].get_net()[0] == net_1 and e[i].get_net()[1] == net_2:
                    e.pop(i)
                    continue
                elif e[i].get_net()[0] == net_2 and e[i].get_net()[1] == net_1:
                    e.pop(i)
                    continue
                else:
                    e[i].property = 0
                    i += 1
            i += 1
        e.append(component_source_v([net_2, net_1], 1))
        solution = calculator.get_linear_complex_solution(e,f)
        Ib = calculator.get_complex_vector_Ib(e)
        i = solution[Ib[-1]]
        y=1j
        i=sympy.re(i)+sympy.im(i)*y
        return -1/i
        
    @staticmethod
    def get_n(e):
        List = set()
        for i in e:
            i.get_n(List)
        return len(List)

    @staticmethod
    def get_b(e):
        return len(e)

    @staticmethod
    def get_matrix_A(e):
        n, b = calculator.get_n(e), calculator.get_b(e)
        A = np.zeros([n, b])
        for i in range(len(e)):
           e[i].get_matrix_A(A,i)
        return A

    @staticmethod
    def get_vector_Usb(e):
        b = calculator.get_b(e)
        Usb = np.zeros([b, 1])
        for i in range(len(e)):
            e[i].get_vector_Usb(Usb,i)
        return Matrix(Usb)

    @staticmethod
    def get_vector_Ub(e):
        b = calculator.get_b(e)
        Str = ''
        for i in range(b):
            Str += "U" + str(i) + ' '
        ub = Matrix(symbols(Str))
        return ub

    @staticmethod
    def get_vector_Zb(e):
        b = calculator.get_b(e)
        Zb = np.zeros([b, b])
        for i in range(len(e)):
            e[i].get_matrix_Zb(Zb,i)
        return Matrix(Zb)

    @staticmethod
    def get_vector_Ib(e):
        b = calculator.get_b(e)
        Str = ''
        for i in range(b):
            Str += "I" + str(i) + ' '
        Ib = Matrix(symbols(Str))
        return Ib

    @staticmethod
    def get_vector_Isb(e):
        b = calculator.get_b(e)
        Isb=np.zeros([b, 1])
        for i in range(len(e)):
            e[i].get_vector_Isb(Isb,i)
        return Matrix(Isb)

    @staticmethod
    def get_matrix_F(e):
        b = calculator.get_b(e)
        F = np.zeros([b, b])
        for i in range(len(e)):
            e[i].get_matrix_F(F,i)
        return F

    @staticmethod
    def get_matrix_H(e):
        b = calculator.get_b(e)
        H = np.zeros([b, b])
        for i in range(len(e)):
            e[i].get_matrix_H(H,i)
        return H

    @staticmethod
    def get_vector_Un(e):
        n = calculator.get_n(e)
        Str = ""
        for i in range(n):
            Str += "Un" + str(i) + ' '
        Un = Matrix(symbols(Str))
        Un[0] = 0
        return Un

    @staticmethod
    def get_linear_solution(e):
        A = Matrix(calculator.get_matrix_A(e))
        F = Matrix(calculator.get_matrix_F(e))
        H = Matrix(calculator.get_matrix_H(e))
        Usb = calculator.get_vector_Usb(e)
        Isb = calculator.get_vector_Isb(e)
        Ib = calculator.get_vector_Ib(e)
        Ub = calculator.get_vector_Ub(e)
        Un = calculator.get_vector_Un(e)
        At = A.transpose()
        eq1, eq2, eq3 = A.multiply(Ib), At.multiply(Un), F.multiply(Ub) + H.multiply(Ib)
        eq = Matrix([[eq1], [eq2], [eq3]])
        eq1_, eq2_, eq3_ = Matrix(np.zeros([eq1.shape[0], 1])), Ub, Usb + Isb
        eq_ = Matrix([[eq1_], [eq2_], [eq3_]])
        eq = Eq(eq, eq_)
        X = Matrix([Ib, Un, Ub])
        solution = solve(eq, X)
        return solution

    @staticmethod
    def get_complex_matrix_F(e,f):
        b = calculator.get_b(e)
        F = Matrix(np.zeros([b, b]))
        for i in range(len(e)):
            e[i].get_complex_F(F, i, f)
        return F
        pass

    @staticmethod
    def get_complex_matrix_H(e,f):
        b = calculator.get_b(e)
        H = Matrix(np.zeros([b, b]))
        for i in range(len(e)):
            e[i].get_complex_H(H, i,f)
        return H

    @staticmethod
    def get_complex_vector_Usb(e,f):
        b = calculator.get_b(e)
        Usb = np.zeros([b, 1])
        for i in range(len(e)):
            e[i].get_vector_Usb(Usb, i)
        return Matrix(Usb)

    @staticmethod
    def get_complex_vector_Isb(e,f):
        b = calculator.get_b(e)
        Isb = np.zeros([b, 1])
        for i in range(len(e)):
            e[i].get_vector_Isb(Isb, i)
        return Matrix(Isb)

    @staticmethod
    def get_complex_vector_Ub(e):
        b = calculator.get_b(e)
        Str = ''
        for i in range(b):
            Str += "U" + str(i) + ' '
        ub = Matrix(symbols(Str,complex=True))
        return ub

    @staticmethod
    def get_complex_vector_Ib(e):
        b = calculator.get_b(e)
        Str = ''
        for i in range(b):
            Str += "I" + str(i) + ' '
        Ib = Matrix(symbols(Str,complex=True))
        return Ib
        pass

    @staticmethod
    def get_complex_vector_Un(e):
        n = calculator.get_n(e)
        Str = ""
        for i in range(n):
            Str += "Un" + str(i) + ' '
        Un = Matrix(symbols(Str,complex=True))
        Un[0] = 0
        return Un
    @staticmethod
    def get_linear_complex_solution(e,f):
        A = Matrix(calculator.get_matrix_A(e))
        F = Matrix(calculator.get_complex_matrix_F(e,f))
        H = Matrix(calculator.get_complex_matrix_H(e,f))
        Usb = calculator.get_complex_vector_Usb(e,f)
        Isb = calculator.get_complex_vector_Isb(e,f)
        Ib = calculator.get_complex_vector_Ib(e)
        Ub = calculator.get_complex_vector_Ub(e)
        Un = calculator.get_complex_vector_Un(e)
        At = A.transpose()
        eq1, eq2, eq3 = A.multiply(Ib), At.multiply(Un), F.multiply(Ub) + H.multiply(Ib)
        eq = Matrix([[eq1], [eq2], [eq3]])
        eq1_, eq2_, eq3_ = Matrix(np.zeros([eq1.shape[0], 1])), Ub, Usb + Isb
        eq_ = Matrix([[eq1_], [eq2_], [eq3_]])
        eq = Eq(eq, eq_)
        X = Matrix([Ib, Un, Ub])
        solution = solve(eq, X)
        return solution
    @staticmethod
    def solution_to_str(solution,e):
        Ib = calculator.get_vector_Ib(e)
        Ub = calculator.get_vector_Ub(e)
        Un = calculator.get_vector_Un(e)
        string=""
        for i in range(len(Ib)):
            string+="I"+str(i)+":"+"{:.2f}".format(solution[Ib[i]])+"A  "+"\n"
        string+="\n"
        for i in range(len(Ub)):
            string+="U"+str(i)+":"+"{:.2f}".format(solution[Ub[i]])+"V  "+"\n"
        string += "\n"
        for i in range(len(Un)):
            string+="Un"+str(i)+":"+"{:.2f}".format(solution[Un[i]])+"V  "+"\n"
        return string
    @staticmethod
    def get_equal_R(e_temp, net_1, net_2):
        import copy
        e = copy.deepcopy(e_temp)
        i = 0
        while i < len(e):
            if e[i].get_kind() == "source_v" :
                if  e[i].get_net()[0]==net_1 and e[i].get_net()[1]==net_2:
                    e.pop(i)
                    continue
                else:
                    e[i].property=0
                    i+=1
            i += 1
        e.append(component_source_v([net_1,net_2],1))
        solution = calculator.get_linear_solution(e)
        Ib = calculator.get_vector_Ib(e)
        #print(solution)
        i = abs(solution[Ib[len(e) - 1]])
        return 1 / i
        pass

    @staticmethod
    def X_t(A,B,x,sti_value):
        return A.multiply(x)+B.multiply(sti_value)

    @staticmethod
    def cal(step, A, B, sti_value, init, t,e):
        L1 = calculator.X_t(A, B, init, sti_value)
        L2 = calculator.X_t(A, B, init + L1 * step / 2, calculator.get_sti_value(e,t))
        L3 = calculator.X_t(A, B, init + L2 * step / 2, calculator.get_sti_value(e,t))
        L4 = calculator.X_t(A, B, init + L3 * step, calculator.get_sti_value(e,t))
        delta = (L1 + L2 * 2 + L3 * 2 + L4) / 6 * step
        return init + delta

    @staticmethod
    def cal_longe(e):
        t=0
        A=Matrix(calculator.get_state_A2(e))
        B=Matrix(calculator.get_state_B(e))
        value=Matrix(calculator.get_init_value(e))
        import matplotlib.pyplot as plt
        re=[]
        for i in range(len(value)):
            re.append([])
        while t<=50:
            for i in range(len(value)):
                re[i].append(value[i])
            sti_value = Matrix(calculator.get_sti_value(e, t))
            #print(sti_value)
            value=calculator.cal(0.01,A,B,sti_value,value,t,e)
            t+=0.01
        X=range(len(re[0]))
        X=[i/100 for i in X]
        for i in range(len(re)):
            plt.plot(X,re[i],label="x"+str(i))
        plt.legend()
        plt.show()

    @staticmethod
    def cal_longe_targeted(e_temp,List_target,T):
        def A(e_temp,List_target):
            def F(A,index,List,List_target,e_temp):
                import copy
                e = copy.deepcopy(e_temp)
                for j in range(len(e)):
                    if List[index] == j or e[j].get_kind() in ["R", "Y"]:
                        continue
                    if e[j].get_kind() in ["source_v", "C"]:
                        e[j] = component_R(e[j].get_net(), 0)
                    if e[j].get_kind() in ["source_i", "L"]:
                        e[j] = component_Y(e[j].get_net(), 0)
                if e[List[index]].get_kind() == "C":
                    e[List[index]] = component_source_v(e[List[index]].get_net(), 1)
                elif e[List[index]].get_kind() == "L":
                    e[List[index]] = component_source_i(e[List[index]].get_net(), 1)
                solution = calculator.get_linear_solution(e)
                Ib = calculator.get_vector_Ib(e)
                Ub = calculator.get_vector_Ub(e)
                for i in range(len(List_target)):
                    if List_target[i][1]=="I":
                        A[i, index] = solution[Ib[List_target[i][0]]]
                    else:
                        A[i, index] = solution[Ub[List_target[i][0]]]
                return A
            List = []
            for i in e_temp:
                List = i.get_state_A2(List)
            List = [index for index, value in enumerate(List) if value in [4, 5]]
            m,n = len(List_target),len(List)
            A = np.zeros([m, n])
            for index in range(n):
                A = F(A, index, List, List_target,e_temp)
            return A
        def B(e_temp,List_target):
            def F2(B, index, List_target, List2, e_temp):
                import copy
                e = copy.deepcopy(e_temp)
                for j in range(len(e)):
                    if List2[index] == j or e[j].get_kind() in ["R", "Y"]:
                        continue
                    if e[j].get_kind() in ["source_v", "C"]:
                        e[j] = component_R(e[j].get_net(), 0)
                    if e[j].get_kind() in ["source_i", "L"]:
                        e[j] = component_Y(e[j].get_net(), 0)
                e[List2[index]].property = 1
                solution = calculator.get_linear_solution(e)
                Ib = calculator.get_vector_Ib(e)
                Ub = calculator.get_vector_Ub(e)
                for i in range(len(List_target)):
                    if List_target[i][1] == "I":
                        B[i, index] = solution[Ib[List_target[i][0]]]
                    else:
                        B[i, index] = solution[Ub[List_target[i][0]]]
                return B
            List = []
            for i in e_temp:
                List_ = i.get_state_A2(List)
            List =List_target
            List2 = [index for index, value in enumerate(List_) if value in [2, 3]]
            n, m = len(List), len(List2)
            B = np.zeros([n, m])
            for i in range(m):
                B = F2(B, i, List, List2, e_temp)
            return B
        A1=Matrix(A(e_temp,List_target))
        B1=Matrix(B(e_temp,List_target))
        A2=Matrix(calculator.get_state_A2(e_temp))
        B2=Matrix(calculator.get_state_B(e_temp))
        value = Matrix(calculator.get_init_value(e_temp))
        sti_value = Matrix(calculator.get_sti_value(e_temp, 0))
        target_value=A1.multiply(value)+B1.multiply(sti_value)
        t=0
        import matplotlib.pyplot as plt
        re = []
        for i in range(len(target_value)):
            re.append([])
        while t <= T:
            for i in range(len(target_value)):
                re[i].append(target_value[i])
            sti_value = Matrix(calculator.get_sti_value(e_temp,t))
            value = calculator.cal(0.01, A2, B2, sti_value, value, t,e_temp)
            target_value=A1.multiply(value)+B1.multiply(sti_value)
            t += 0.01
        X = range(len(re[0]))
        X = [i / 100 for i in X]
        for i in range(len(re)):
            label=List_target[i][1]+str(List_target[i][0])
            plt.plot(X,re[i],label=label)
        #plt.plot(X, re, label="x1")
        #plt.plot(X, re2, label="x2")
        plt.xlabel("t / s")
        plt.ylabel("U / V\nI / A")
        plt.legend()
        plt.show()


    @staticmethod
    def get_state_n(e):
        a=0
        for i in e:
            a=i.get_sti_n()
        return a

    @staticmethod
    def get_List_R(e):
        List=[]
        for i in range(len(e)):
            List=e[i].get_R()
        return List
        pass

    @staticmethod
    def get_state_A(e_temp):
        List_R = []
        List_S = []
        List_X = []
        for i in e_temp:
            List_R ,List_S,List_X=i.get_List_R(List_R),i.get_List_S(List_S),i.get_List_X(List_X)
        return len(List_X)

    @staticmethod
    def F(A,i,List,e_temp):
        import copy
        k=i
        i=List[i]
        mylist=List
        e=copy.deepcopy(e_temp)
        for j in range(len(e)):
            if i==j or e[j].get_kind() in ["R","Y"]:
                continue
            if e[j].get_kind() in ["source_v","C"]:
                e[j]=component_R(e[j].get_net(),0)
            if e[j].get_kind() in ["source_i","L"]:
                e[j]=component_Y(e[j].get_net(),0)
        if e[i].get_kind() == "C":
            e[i] = component_source_v(e[i].get_net(), 1)
        elif e[i].get_kind() == "L":
            e[i] = component_source_i(e[i].get_net(), 1)
        solution=calculator.get_linear_solution(e)
        Ib=calculator.get_vector_Ib(e)
        Ub=calculator.get_vector_Ub(e)
        for j in range(len(mylist)):
            A[j,k]=solution[Ib[mylist[j]]] if e_temp[mylist[j]].get_kind() == "C" else solution[Ub[mylist[j]]]
            A[j,k]=A[j,k]/e_temp[mylist[j]].property
        return A

    @staticmethod
    def get_state_A2(e_temp):
        List=[]
        for i in e_temp:
            List=i.get_state_A2(List)
        List=[index for index,value in enumerate(List) if value in [4,5]]
        n = len(List)
        A = np.zeros([n, n])
        for i in range(n):
            A=calculator.F(A,i,List,e_temp)
        return A

    @staticmethod
    def F2(B,index,List,List2,e_temp):
        import copy
        e=copy.deepcopy(e_temp)
        for j in range(len(e)):
            if List2[index] == j or e[j].get_kind() in ["R", "Y"]:
                continue
            if e[j].get_kind() in ["source_v", "C"]:
                e[j] = component_R(e[j].get_net(), 0)
            if e[j].get_kind() in ["source_i", "L"]:
                e[j] = component_Y(e[j].get_net(), 0)
        e[List2[index]].property=1
        solution = calculator.get_linear_solution(e)
        Ib = calculator.get_vector_Ib(e)
        Ub = calculator.get_vector_Ub(e)
        for j in range(len(List)):
            B[j, index] = solution[Ib[List[j]]] if e_temp[List[j]].get_kind() == "C" else solution[Ub[List[j]]]
            B[j, index] = B[j, index] / e_temp[List[j]].property
        return B

    @staticmethod
    def get_state_B(e_temp):
        List = []
        for i in e_temp:
            List_ = i.get_state_A2(List)
        List = [index for index, value in enumerate(List_) if value in [4, 5]]
        List2 = [index for index, value in enumerate(List_) if value in [2, 3]]
        n,m= len(List),len(List2)
        B = np.zeros([n, m])
        for i in range(m):
            B=calculator.F2(B,i,List,List2,e_temp)
        return B

    @staticmethod
    def get_init_value(e_temp):
        List_ = []
        for i in e_temp:
            List_ = i.get_state_A2(List_)
        List = [index for index, value in enumerate(List_) if value in [4, 5]]
        init_value=np.zeros([len(List),1])
        for i in range(len(List)):
            init_value[i,0]=e_temp[List[i]].get_init_value()
        return init_value

    @staticmethod
    def get_sti_value(e_temp,t):
        List_ = []
        for i in e_temp:
            List_ = i.get_state_A2(List_)
        List = [index for index, value in enumerate(List_) if value in [2,3]]
        sti_value = np.zeros([len(List), 1])
        for i in range(len(List)):
            sti_value[i, 0] = e_temp[List[i]].get_sti_value(t)
        return sti_value
class switch():
    @staticmethod
    def solution_complexstr(solution,e):
        Ib = calculator.get_complex_vector_Ib(e)
        Ub = calculator.get_complex_vector_Ub(e)
        Un = calculator.get_complex_vector_Un(e)
        string=''
        for i in range(len(Ib)):
            ab=abs(solution[Ib[i]])
            ar=sympy.arg(solution[Ib[i]])
            ar=ar*180/np.pi
            ab=np.format_float_positional(ab,precision=3,unique=False,fractional=False,trim='k')
            ar=np.format_float_positional(ar,precision=3,unique=False,fractional=False,trim='k')
            string+="I"+str(i)+":"+str(ab)+"\u2220"+str(ar)+"\u00B0"+"A\n"
        string+='\n'
        for i in range(len(Ub)):
            ab=abs(solution[Ub[i]])
            ar=sympy.arg(solution[Ub[i]])
            ar = ar * 180 / np.pi
            ab=np.format_float_positional(ab,precision=3,unique=False,fractional=False,trim='k')
            ar=np.format_float_positional(ar,precision=3,unique=False,fractional=False,trim='k')
            string+="U"+str(i)+":"+str(ab)+"\u2220"+str(ar)+"\u00B0"+"V\n"
        string+='\n'
        for i in range(len(Un)):
            ab=abs(solution[Un[i]])
            ar=sympy.arg(solution[Un[i]]) if i!=0 else 0
            ar = ar * 180 / np.pi
            ab=np.format_float_positional(ab,precision=3,unique=False,fractional=False,trim='k')
            ar=np.format_float_positional(ar,precision=3,unique=False,fractional=False,trim='k')
            string+="Un"+str(i)+":"+str(ab)+"\u2220"+str(ar)+"\u00B0"+"V\n"
        return string
    
    @staticmethod
    def switch_List(List):
        def add_e(List):
            if List[0]==1:
                return component_source_v(List[2],List[1])
            elif List[0]==2:
                return component_source_i(List[2],List[1])
            elif List[0]==3:
                return component_R(List[2],List[1])
            elif List[0]==4:
                return component_C(List[2],List[1])
            elif List[0]==5:
                return component_L(List[2],List[1])
        def bfs(Set,List,local):
            array=[2,1]
            net=array[local[1]-1]
            newnode=(local[0],net)
            for i in Set:
                if newnode in i:
                    n1=len(i)
                    for value in List[local[0]][2][net-1]:
                        i.add((value[0],value[1]))
                    n1=n1-len(i)
                    if n1==0:
                        return Set
                    for value in copy.deepcopy(i):
                        Set=bfs(Set,List,value)
                    return Set
            set1=set()
            set1.add(newnode)
            for i in List[local[0]][2][net-1]:
                set1.add((i[0],i[1]))
            Set.append(set1)
            for value in copy.deepcopy(set1):
                Set=bfs(Set,List,value)
            return Set
        def get_index(locate,Set):
            for i in range(len(Set)):
                if locate in Set[i]:
                    return i
            return -1
            pass
        def pop(Set,index):
            for i in range(len(Set)):
                if (index,2) in Set[i]:
                    Set.pop(i)
                    return Set
        e,index=[],-1
        for i in range(len(List)):
            if List[i][0]==0:
                index=i
        Set=[set()]
        for i in List[index][2][0]:
            Set[0].add((i[0],i[1]))
        for i in copy.deepcopy(Set[0]):
            Set=bfs(Set,List,i)
        Set = pop(Set, index)
        for i in range(len(List)):
            if i==index:
                continue
            List[i][2][0]=get_index((i,1),Set)
            List[i][2][1]=get_index((i,2),Set)
        for i in range(len(List)):
            if index==i:
                continue
            else:
                e.append(add_e(List[i]))#设置e的元素，未命名节点
        return e
    @staticmethod
    def assume_net(List):
        def add_e(List):
            if List[0]==1:
                return component_source_v(List[2],List[1])
            elif List[0]==2:
                return component_source_i(List[2],List[1])
            elif List[0]==3:
                return component_R(List[2],List[1])
            elif List[0]==4:
                return component_C(List[2],List[1])
            elif List[0]==5:
                return component_L(List[2],List[1])
        def bfs(Set,List,local):
            array=[2,1]
            net=array[local[1]-1]
            newnode=(local[0],net)
            for i in Set:
                if newnode in i:
                    n1=len(i)
                    for value in List[local[0]][2][net-1]:
                        i.add((value[0],value[1]))
                    n1=n1-len(i)
                    if n1==0:
                        return Set
                    for value in copy.deepcopy(i):
                        Set=bfs(Set,List,value)
                    return Set
            set1=set()
            set1.add(newnode)
            for i in List[local[0]][2][net-1]:
                set1.add((i[0],i[1]))
            Set.append(set1)
            for value in copy.deepcopy(set1):
                Set=bfs(Set,List,value)
            return Set
        def get_index(locate,Set):
            for i in range(len(Set)):
                if locate in Set[i]:
                    return i
            return -1
            pass
        def pop(Set,index):
            for i in range(len(Set)):
                if (index,2) in Set[i]:
                    Set.pop(i)
                    return Set
        index=[],-1
        for i in range(len(List)):
            if List[i][0]==0:
                index=i
        Set=[set()]
        for i in List[index][2][0]:
            Set[0].add((i[0],i[1]))
        for i in copy.deepcopy(Set[0]):
            Set=bfs(Set,List,i)
        Set = pop(Set, index)
        for i in range(len(List)):
            if i==index:
                continue
            List[i][2][0]=get_index((i,1),Set)
            List[i][2][1]=get_index((i,2),Set)
        # print(List)
        return List
class apply():
    
    @staticmethod
    def print_s(e):
        print("eee")
        for i in e:
            print("net:",i.get_net()," kind:",i.get_kind()," property:",i.property)
    
    @staticmethod
    def max_power_law(e,index,step,first,end,w):
        net1 = e[index].get_net()[0]
        net2 = e[index].get_net()[1]
        e_temp = copy.deepcopy(e)
        e_temp[index] = component_Y(e[index].get_net(), 0)
        eq_R = calculator.get_equal_complex_R(e_temp, net1, net2,w)
        eq1,eq2=sympy.re(eq_R),sympy.im(eq_R)
        
        eq_R= np.format_float_positional(abs(eq_R), precision=3, unique=False, fractional=False, trim='k')
        eq1= np.format_float_positional(eq1, precision=3, unique=False, fractional=False, trim='k')
        eq2= np.format_float_positional(eq2, precision=3, unique=False, fractional=False, trim='k')
        #print(eq_R)
        e[index].property = first
        y1, y2, y3 = [], [], []
        for i in np.arange(first, end, step):
            e[index].property = i
            solution = calculator.get_linear_complex_solution(e,w)
            #print(solution)
            Ib = calculator.get_complex_vector_Ib(e)
            Ub = calculator.get_complex_vector_Ub(e)
            y1.append(solution[Ib[index]])
            y2.append(solution[Ub[index]])
            y3.append(abs(solution[Ib[index]])*abs(solution[Ub[index]]))
        x = np.arange(first, end, step)
        for i in range(len(x)):
            print(str(x[i])+' '+str(y3[i]))
        plt.plot(x, y3,label=str(eq1)+"+"+str(eq2)+"i"+"\n"+str(eq_R))
        plt.title("P-R")
        plt.ylim(bottom=0)
        plt.ylabel("P / W")
        plt.xlabel("R / Ω")
        plt.legend()
        plt.show()
        pass
    
    @staticmethod
    def ana_daiweinan(e,index,step,first,end):
        net1=e[index].get_net()[0]
        net2=e[index].get_net()[1]
        e_temp=copy.deepcopy(e)
        e_temp[index]=component_Y(e[index].get_net(),0)
        eq_R=calculator.get_equal_R(e_temp,net1,net2)
        print(eq_R)
        e[index].property=first
        y1,y2,y3=[],[],[]
        for i in np.arange(first,end,step):
            e[index].property=i
            solution = calculator.get_linear_solution(e)
            Ib = calculator.get_vector_Ib(e)
            Ub = calculator.get_vector_Ub(e)
            y1.append(solution[Ib[index]])
            y2.append(solution[Ub[index]])
            #y3.append(solution[Ib[index]]*solution[Ub[index]])
        x=np.arange(first,end,step)
        #plt.plot(x,y1,label="I")
        plt.plot(y1, y2)
        plt.title("U-I")
        plt.ylim(bottom=0)
        plt.ylabel("U / V")
        plt.xlabel("I / A")
        plt.legend()
        plt.show()
        pass
if __name__ == "__main__":
#元件种类是1 - 电压源    2 - 电流源    3 - 电阻   4 - 电容   5 - 电感   0 - 接地
     e1=componnet_fang_source_v([1,0],[1,5])
     e2=component_C([1,2],1)
     e3=component_R([2,0],6)
     e=[e1,e2,e3]
     calculator.cal_longe(e)
     '''List=[[1, 5, [[[2, 1], [1, 1]], [[4, 1]]]], [3, 10, [[[0, 1]], [[3, 1]]]], [3, 10, [[[0, 1]], [[3, 1]]]], [3, 10, [[[1, 2], [2, 2]], [[4, 2]]]], [3, 10, [[[0, 2], [5, 1]], [[3, 2]]]], [0, None, [[[4, 1]], []]]]
   e=switch.switch_List(copy.deepcopy(List))
   apply.ana_daiweinan(e,1,0.2,1,10)'''




