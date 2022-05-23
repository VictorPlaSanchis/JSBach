~~~ VICTOR PLA i SANCHIS - MERGE SORT ~~~

Main |:
    l <- { }
    while #l <= 51 |:
        l << (51 - #l)
    :|
    <!> "Initial list: " l
    Sort l
    <!> "Sorted list: " l

    ~~~ COMPROBEM QUE ESTA ORDENAT CRIDANT A CHECK SORT, RECORRA TOT EL VECTOR! ~~~
    ~~~ HEM GUARDAT check COM A VECTOR AIXI CheckSort EL MODIFICA COM A REFERENCIA I EL PODEM RECUPERAR AL MAIN! ~~~
    check <- { true }
    CheckSort check l
    ~~~ RECUPEREM check MODIFICAT PER REFERENCIA A CheckSort ~~~
    isChecked <- check[1]
    if isChecked |: <!> "Sha comprobat que esta ordenat!" :| 
    else |: <!> "Algo a fallat! :( El vector no sha ordenat correctament." :|

:|

CheckSort result arr |:
    i <- 2
    result <- { true }
    while i <= #arr |:
        if arr[i] <= arr[i-1] |: result <- { false } :|
        if arr[i] < 52 |:
            <:> arr[i]
        :|
        i <- i + 1
    :|
:|

Sort a |:
    if #a > 1 |:
        b <- {}
        c <- {}
        DivArray a b c
        Sort b
        Sort c
        Merge a b c
    :|
:|

Merge a b c |:
    ib <- 1
    ic <- 1
    a <- {}
    sizeMin <- 0
    notBreak <- true
    if #b < #c |: sizeMin <- #b :| else |: sizeMin <- #c :|
    while notBreak |:
        if b[ib] < c[ic] |:
            a << b[ib]
            ib <- ib + 1
        :| else |:
            a << c[ic]
            ic <- ic + 1
        :|

        if ib > #b |: notBreak <- false :|
        if ic > #c |: notBreak <- false :|

    :|

    if ib > #b |: 
        while ic <= #c |: 
            a << c[ic] 
            ic <- ic + 1
        :|
    :| else |: 
        while ib <= #b |: 
            a << b[ib] 
            ib <- ib + 1
        :|
    :|
:|

DivArray a b c |:
    size <- #a
    midle <- size / 2
    i <- 1
    while i <= midle |:
        b << a[i]
        i <- i + 1
    :|
    while i <= #a |:
        c << a[i]
        i <- i + 1
    :|
:|