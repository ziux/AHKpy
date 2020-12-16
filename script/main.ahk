#Include %A_LineFile%\..\JSON.ahk

#Include %A_LineFile%\..\func.ahk



EnvGet,FrequencyTimeout ,"FrequencyTimeout"
if(!FrequencyTimeout){
FrequencyTimeout:=400
}
inputFile := "./input"
outputFile := "./output"
Loop
{
    FileGetSize,size,%inputFile%
    if (size>0){

    file := FileOpen(inputFile, "r")
    Text:=file.Read()
    InputObj:=JSON.Load(Text)
    file.Close()
    f := FileOpen(inputFile, "w")
    f.Close()
    fn := Func(InputObj.func)
    args:=InputObj.args
    OutObj:=fn.Call(args*)
    if (InputObj.results == 1){
    out:=FileOpen(outputFile, "w")
    p:=JSON.Dump(OutObj)
    out.Write(p)
    ToolTip %p%,0,0
    out.Close()
    }
    }
    sleep,%FrequencyTimeout%
}


#Include %A_LineFile%\..\hotkey.ahk