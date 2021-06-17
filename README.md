
# NLP-HK202

Đề bài: Xây dựng hệ thống hỏi đáp đơn giản về các chuyến xe bus liên tỉnh bằng Quan hệ văn phạm


# USAGE

## Chạy kiểm tra
```
python main.py --question_file=file_name --grammar=your_grammar
```

## Yêu cầu

```
Python                  3.7
NLTK                    3.6.2
spacy                   2.2.3
spacy-legacy            3.0.5
vi-spacy-model          0.2.1

```


# MODEL
Thứ tự tiến hành như sau:

**Bước 1**: Loại bỏ dấu (?, :, .) trong câu

**Bước 2**: Phân tách các token 

+ Sử dụng thư viện ở đây https://github.com/trungtv/vi_spacy

**Bước 3**: Gán nhãn để xây dựng văn phạm phụ thuộc

+ hàm *spacy_viet* trong *model.py*

**Bước 4**: Tạo dạng luận lý

+ hàm *parserGSVfeature* trong *model.py*

+ Ngoài việc trả về dạng luận lý, ta còn thu được gap và var tương ứng phục vụ cho các bước tiếp theo

**Bước 5**: Tạo ngữ nghĩa thủ tục từ dạng luận lý

+ hàm *convert_featstructures_to_procedure* trong *model.py*

**Bước 6**: Truy xuất cơ sở dữ liệu cho câu truy vấn tương ứng.

+ hàm *retrieve_result* trong trong *model.py*

# INPUT - OUTPUT tương ứng

## CÂU 1: Xe bus nào đến thành phố Huế lúc 20:00HR ?

**output_a.txt**
```
Grammar with 100 productions (start state = S[])
    S[GAP=?f, SEM=<WHQUERY(?vp(?v,?f),?np,?whq(?f))>, VAR=?v] -> WHICH-QUERY[SEM=?whq] BUS-NP[SEM=?np, VAR=?f] BUS-VP[SEM=?vp, VAR=?v]
    S[GAP='t1', SEM=<WHQUERY(?vp(?v,?f,t1),?np,?whq(t1))>, VAR=?v] -> TIME-QUERY[SEM=?whq] BUS-NP[SEM=?np, VAR=?f] BUS-VP[SEM=?vp, VAR=?v]
    S[GAP=?r, SEM=<WHQUERY(?vp,?np,?whq(?f))>, VAR=?v] -> HOW-LONG-QUERY[SEM=?whq, VAR=?r] BUS-NP[SEM=?np, VAR=?f] BUS-VP[SEM=?vp, VAR=?v]
    BUS-NP[SEM=<?det(?cnp)>, VAR=?v] -> DET[SEM=?det] BUS-CNP[SEM=?cnp, VAR=?v]
    BUS-NP[SEM=?cnp, VAR=?v] -> BUS-CNP[SEM=?cnp, VAR=?v]
    BUS-CNP[SEM=<(?cnp & ?dest(?v))>, VAR=?v] -> BUS-CNP[SEM=?cnp, VAR=?v] BUS-DEST[SEM=?dest]
    BUS-CNP[SEM=<(?cnp & ?source(?v))>, VAR=?v] -> BUS-CNP[SEM=?cnp, VAR=?v] BUS-SOURCE[SEM=?source]
    BUS-CNP[SEM=<(?cnp & ?x)>, VAR=?k] -> BUS-CNP[SEM=?cnp, VAR=?v] BUS-NAME-NP[SEM=?x, VAR=?k]
    BUS-CNP[SEM=<?n(?v)>, VAR=?v] -> BUS-N[SEM=?n, VAR=?v]
    BUS-TIME[SEM=<TIME(?v,?time)>, VAR=?v] -> TIME-MOD[SEM=?time, VAR=?v]
    BUS-TIME[SEM=<TIME(?v,?time)>, VAR=?v] -> P-TIME[SEM=?p] TIME-MOD[SEM=?time, VAR=?v]
    BUS-VP[SEM=<\r f t.?v(r,f,TIME(t))>, VAR=?r] -> BUS-V[SEM=?v, VAR=?r]
    BUS-VP[SEM=<\r f.?v(r,f,?time)>, VAR=?r] -> BUS-V[SEM=?v, VAR=?r] BUS-TIME[SEM=?time]
    BUS-VP[SEM=<?cvp>, VAR=?v] -> BUS-CVP[SEM=?cvp, VAR=?v]
    BUS-CVP[SEM=<(?cvp & ?cvpp)>, VAR=?n] -> BUS-CVP[SEM=?cvp, VAR=?n] BUS-CVP[SEM=?cvpp, VAR=?k]
    BUS-CVP[SEM=?cvp, VAR=?n] -> BUS-CVP-DEST[SEM=?cvp, VAR=?n]
    BUS-CVP[SEM=?cvp, VAR=?n] -> BUS-CVP-SOURCE[SEM=?cvp, VAR=?n]
    BUS-CVP-DEST[SEM=<(?v(?n) & ?dest(?v))>, VAR=?n] -> BUS-V[SEM=?v, VAR=?n] BUS-DEST[SEM=?dest]
    BUS-CVP-SOURCE[SEM=<(?v(?n) & ?source(?v))>, VAR=?n] -> BUS-V[SEM=?v, VAR=?n] BUS-SOURCE[SEM=?source]
    BUS-V[SEM=<\r f t.?v(r,f,t)>, VAR=?r] -> ARRIVE-V[SEM=?v, VAR=?r]
    BUS-V[SEM=<\r f t.?v(r,f,t)>, VAR=?r] -> DEPARTURE-V[SEM=?v, VAR=?r]
    ARRIVE-V[SEM=<\r f t.ARRIVE1(r,f,t)>, VAR=<a1>] -> 'arrives'
    ARRIVE-V[SEM=<\r f t.ARRIVE1(r,f,t)>, VAR=<a1>] -> 'arrive'
    DEPARTURE-V[SEM=<\r f t.DEPART1(r,f,t)>, VAR=<d1>] -> 'departs'
    DEPARTURE-V[SEM=<\r f t.DEPART1(r,f,t)>, VAR=<d1>] -> 'depart'
    CITY-NP[SEM=<NAME(?v,?x)>, VAR=?v] -> CITY-NAME[SEM=?x, VAR=?v] CITY-N[SEM=?n]
    CITY-NP[SEM=<DET(?x)>, VAR=?v] -> DET[SEM=?det] CITY-N[SEM=?x, VAR=?v]
    BUS-NAME-NP[SEM=<BUSNAME(?v,?x)>, VAR=?v] -> BUS-NAME[SEM=?x, VAR=?v]
    BUS-SOURCE[SEM=<(\f.SOURCE(f)(?y))(?x)>, VAR=?y] -> 'from' CITY-NP[SEM=?x, VAR=?y]
    BUS-DEST[SEM=<\f.DEST(f,?x)>, VAR=?y] -> 'to' CITY-NP[SEM=?x, VAR=?y]
    BUS-DEST[SEM=<\f.DEST(f,?x)>, VAR=?y] -> 'for' CITY-NP[SEM=?x, VAR=?y]
    BUS-DEST[SEM=<\f.DEST(f,?x)>, VAR=?y] -> 'in' CITY-NP[SEM=?x, VAR=?y]
    TIME-QUERY[SEM=<\x.WH(x,WHAT1)>] -> 'What' 'time' 'does'
    TIME-QUERY[SEM=<\x.WH(x,WHEN1)>] -> 'When' 'does'
    WHICH-QUERY[SEM=<\x.WH(x,WHICH1)>] -> 'Which'
    HOW-LONG-QUERY[SEM=<\x.WH(x,HOWLONG1)>, VAR=<r1>] -> 'How' 'long' 'does'
    DET[SEM=<THE>] -> 'the'
    BUS-N[SEM=<BUS1>, VAR=<f1>] -> 'bus'
    BUS-N[SEM=<BUS1>, VAR=<f1>] -> 'buses'
    P-TIME[SEM=<AT>] -> 'at'
    P-TIME[SEM=<ON>] -> 'on'
    P-TIME[SEM=<IN>] -> 'in'
    CITY-NAME[SEM=<'HCMC'>, VAR=<h1>] -> 'Hồ' 'Chí' 'Minh'
    CITY-NAME[SEM=<'HUE'>, VAR=<h2>] -> 'Huế'
    CITY-NAME[SEM=<'DANANG'>, VAR=<h3>] -> 'Đà' 'Nẵng'
    BUS-NAME[SEM=<'B1'>, VAR=<h4>] -> 'B1'
    BUS-NAME[SEM=<'B2'>, VAR=<h5>] -> 'B2'
    BUS-NAME[SEM=<'B3'>, VAR=<h6>] -> 'B3'
    BUS-NAME[SEM=<'B4'>, VAR=<h7>] -> 'B4'
    BUS-NAME[SEM=<'B5'>, VAR=<h8>] -> 'B5'
    BUS-NAME[SEM=<'B6'>, VAR=<h9>] -> 'B6'
    CITY-N[SEM=<CITY>, VAR=<c1>] -> 'city'
    TIME-MOD[SEM=<0:00HR>, VAR=<t1>] -> '0:00HR'
    TIME-MOD[SEM=<0:30HR>, VAR=<t1>] -> '0:30HR'
    TIME-MOD[SEM=<1:00HR>, VAR=<t1>] -> '1:00HR'
    TIME-MOD[SEM=<1:30HR>, VAR=<t1>] -> '1:30HR'
    TIME-MOD[SEM=<2:00HR>, VAR=<t1>] -> '2:00HR'
    TIME-MOD[SEM=<2:30HR>, VAR=<t1>] -> '2:30HR'
    TIME-MOD[SEM=<3:00HR>, VAR=<t1>] -> '3:00HR'
    TIME-MOD[SEM=<3:30HR>, VAR=<t1>] -> '3:30HR'
    TIME-MOD[SEM=<4:00HR>, VAR=<t1>] -> '4:00HR'
    TIME-MOD[SEM=<4:30HR>, VAR=<t1>] -> '4:30HR'
    TIME-MOD[SEM=<05:00HR>, VAR=<t1>] -> '05:00HR'
    TIME-MOD[SEM=<5:30HR>, VAR=<t1>] -> '5:30HR'
    TIME-MOD[SEM=<6:00HR>, VAR=<t1>] -> '6:00HR'
    TIME-MOD[SEM=<6:30HR>, VAR=<t1>] -> '6:30HR'
    TIME-MOD[SEM=<7:00HR>, VAR=<t1>] -> '7:00HR'
    TIME-MOD[SEM=<7:30HR>, VAR=<t1>] -> '7:30HR'
    TIME-MOD[SEM=<8:00HR>, VAR=<t1>] -> '8:00HR'
    TIME-MOD[SEM=<8:30HR>, VAR=<t1>] -> '8:30HR'
    TIME-MOD[SEM=<9:00HR>, VAR=<t1>] -> '9:00HR'
    TIME-MOD[SEM=<9:30HR>, VAR=<t1>] -> '9:30HR'
    TIME-MOD[SEM=<10:00HR>, VAR=<t1>] -> '10:00HR'
    TIME-MOD[SEM=<10:30HR>, VAR=<t1>] -> '10:30HR'
    TIME-MOD[SEM=<11:00HR>, VAR=<t1>] -> '11:00HR'
    TIME-MOD[SEM=<11:30HR>, VAR=<t1>] -> '11:30HR'
    TIME-MOD[SEM=<12:00HR>, VAR=<t1>] -> '12:00HR'
    TIME-MOD[SEM=<12:30HR>, VAR=<t1>] -> '12:30HR'
    TIME-MOD[SEM=<13:00HR>, VAR=<t1>] -> '13:00HR'
    TIME-MOD[SEM=<13:30HR>, VAR=<t1>] -> '13:30HR'
    TIME-MOD[SEM=<14:00HR>, VAR=<t1>] -> '14:00HR'
    TIME-MOD[SEM=<14:30HR>, VAR=<t1>] -> '14:30HR'
    TIME-MOD[SEM=<15:00HR>, VAR=<t1>] -> '15:00HR'
    TIME-MOD[SEM=<15:30HR>, VAR=<t1>] -> '15:30HR'
    TIME-MOD[SEM=<16:00HR>, VAR=<t1>] -> '16:00HR'
    TIME-MOD[SEM=<16:30HR>, VAR=<t1>] -> '16:30HR'
    TIME-MOD[SEM=<17:00HR>, VAR=<t1>] -> '17:00HR'
    TIME-MOD[SEM=<17:30HR>, VAR=<t1>] -> '17:30HR'
    TIME-MOD[SEM=<18:00HR>, VAR=<t1>] -> '18:00HR'
    TIME-MOD[SEM=<18:30HR>, VAR=<t1>] -> '18:30HR'
    TIME-MOD[SEM=<19:00HR>, VAR=<t1>] -> '19:00HR'
    TIME-MOD[SEM=<19:30HR>, VAR=<t1>] -> '19:30HR'
    TIME-MOD[SEM=<20:00HR>, VAR=<t1>] -> '20:00HR'
    TIME-MOD[SEM=<20:30HR>, VAR=<t1>] -> '20:30HR'
    TIME-MOD[SEM=<21:00HR>, VAR=<t1>] -> '21:00HR'
    TIME-MOD[SEM=<21:30HR>, VAR=<t1>] -> '21:30HR'
    TIME-MOD[SEM=<22:00HR>, VAR=<t1>] -> '22:00HR'
    TIME-MOD[SEM=<22:30HR>, VAR=<t1>] -> '22:30HR'
    TIME-MOD[SEM=<23:00HR>, VAR=<t1>] -> '23:00HR'
    TIME-MOD[SEM=<23:30HR>, VAR=<t1>] -> '23:30HR'

```

**output_b.txt**

![image](https://user-images.githubusercontent.com/60598942/122389947-fe963900-cf60-11eb-90e8-b20ec1caafd0.png)

```
Token def.
a. token.text, b. token.lemma_, c. token.pos_, d. token.tag_, e. token.dep_, f.token.shape_, g. token.is_alpha, h. token.is_stop
0. a.Thời_gian, b.Thời_gian, c.X, d.N, e.dep, f.xxxxxxxxx, g.False, h.True
1. a.xe, b.xe, c.X, d.N, e.nsubj, f.xx, g.True, h.False
2. a.bus, b.bus, c.X, d.V, e.xcomp, f.xxx, g.True, h.False
3. a.B1, b.B1, c.X, d.Ny, e.obj, f.xx, g.False, h.False
4. a.từ, b.từ, c.X, d.E, e.case, f.xx, g.True, h.True
5. a.Hồ_Chí_Minh, b.Hồ_Chí_Minh, c.X, d.Np, e.obl, f.xxxxxxxxxxx, g.False, h.False
6. a.đến, b.đến, c.X, d.V, e.ROOT, f.xxx, g.True, h.True
7. a.Huế, b.Huế, c.X, d.Np, e.obj, f.xxx, g.True, h.False


```


**output_c.txt**

```
[Tree('đến_V_ROOT', ['Thời_gian_N_dep', Tree('xe_N_nsubj', [Tree('bus_V_xcomp', ['B1_Ny_obj', Tree('Hồ_Chí_Minh_Np_obl', ['từ_E_case'])])]), 'Huế_Np_obj'])]

```

**output_d.txt**
```
[         [      [       [ bus     = 'f2'            ] ]                 ] ]
[         [ np = [ the = [                           ] ]                 ] ]
[         [      [       [ busname = [ h    = 'h3' ] ] ]                 ] ]
[         [      [       [           [ name = 'B1' ] ] ]                 ] ]
[         [                                                              ] ]
[         [      [          [ a = 'a3'                   ]             ] ] ]
[         [      [          [ f = 'f2'                   ]             ] ] ]
[         [      [ arrive = [                            ]             ] ] ]
[         [      [          [ t = [ t_var    = '?t'    ] ]             ] ] ]
[         [      [          [     [ time_var = '?time' ] ]             ] ] ]
[         [      [                                                     ] ] ]
[         [      [          [ d = 'd3'                   ]             ] ] ]
[         [      [          [ f = 'f1'                   ]             ] ] ]
[         [      [ depart = [                            ]             ] ] ]
[ query = [      [          [ t = [ t_var    = '?t'    ] ]             ] ] ]
[         [ vp = [          [     [ time_var = '?time' ] ]             ] ] ]
[         [      [                                                     ] ] ]
[         [      [          [            [ f    = 'h1'             ] ] ] ] ]
[         [      [ dest   = [ destName = [                         ] ] ] ] ]
[         [      [          [            [ name = [ h    = 'h6'  ] ] ] ] ] ]
[         [      [          [            [        [ name = 'Huế' ] ] ] ] ] ]
[         [      [                                                     ] ] ]
[         [      [          [ bus        = 'h4'                     ]  ] ] ]
[         [      [ source = [                                       ]  ] ] ]
[         [      [          [ sourceName = [ f    = 'h4'          ] ]  ] ] ]
[         [      [          [              [ name = 'Hồ_Chí_Minh' ] ]  ] ] ]
[         [                                                              ] ]
[         [ wh = [ whType = [ f    = 'h1'       ] ]                      ] ]
[         [      [          [ type = 'HOWLONG1' ] ]                      ] ]

```


**output_e.txt**
```
(PRINT-ALL ?r2(BUS ?f2)(ATIME ?f2 HUE ?time)(DTIME ?f2 HCMC ?td)(RUNTIME ?f2 B1 HCMC HUE))

```

**output_f.txt**
```
9:00HR

```


## CÂU 2: Thời gian xe bus B3 từ Đà Nẵng đến Huế ?

[ANSWER](https://github.com/thanh-pham2k/NLP-HK202/tree/main/output/question_2)


## CÂU 3: Xe bus nào đến thành phố Hồ Chí Minh ?

[ANSWER](https://github.com/thanh-pham2k/NLP-HK202/tree/main/output/question_3)

Các câu mở rộng

## CÂU 4: Xe bus nào đến thành phố Hà Nội ?

[ANSWER](https://github.com/thanh-pham2k/NLP-HK202/tree/main/output/question_4)


## CÂU 5: Thời gian xe bus B1 từ Hồ Chí Minh đến Huế ?

[ANSWER](https://github.com/thanh-pham2k/NLP-HK202/tree/main/output/question_5)



# Cấu trúc thư mục

```bash
├── input
│   ├── question_1.txt
│   ├── question_2.txt
│   ├── question_3.txt
│   ├── question_4.txt
│   ├── question_5.txt
├── output
│   ├── question_1
│   ├───────├──output_a.txt
│   ├───────├──output_b.txt
│   ├───────├──output_c.txt
│   ├───────├──output_d.txt
│   ├───────├──output_e.txt
│   ├───────├──output_f.txt
│   ├── question_2
│   ├───────├──output_a.txt
│   ├───────├──output_b.txt
│   ├───────├──output_c.txt
│   ├───────├──output_d.txt
│   ├───────├──output_e.txt
│   ├───────├──output_f.txt
│   ├── question_3
│   ├───────├──output_a.txt
│   ├───────├──output_b.txt
│   ├───────├──output_c.txt
│   ├───────├──output_d.txt
│   ├───────├──output_e.txt
│   ├───────├──output_f.txt
│   ├── question_4
│   ├───────├──output_a.txt
│   ├───────├──output_b.txt
│   ├───────├──output_c.txt
│   ├───────├──output_d.txt
│   ├───────├──output_e.txt
│   ├───────├──output_f.txt
│   ├── question_5
│   ├───────├──output_a.txt
│   ├───────├──output_b.txt
│   ├───────├──output_c.txt
│   ├───────├──output_d.txt
│   ├───────├──output_e.txt
│   ├───────├──output_f.txt

├── grammar.fcfg
├── main.py
├── model.py
├── util.py
```


# NLP-HK-202-TEMP
