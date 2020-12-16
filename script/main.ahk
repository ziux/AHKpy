#InstallKeybdHook
#InstallMouseHook
#Include %A_LineFile%\..\JSON.ahk

#Include %A_LineFile%\..\func.ahk
#Include %A_LineFile%\..\base.ahk


Loop
{
    ;FileGetSize,size,%inputFile%
    if (!inputFile.AtEOF){
    Content:=inputFile.Read()
    Loop, parse, Content, `n, `r
   {
    Text=%A_LoopField%
    InputObj:=JSON.Load(Text)
    fn := Func(InputObj.func)
    args:=InputObj.args
    OutObj:=fn.Call(args*)
    if (InputObj.results == 1){

        j:={results:OutObj,uuid:InputObj.uuid}
        p:=JSON.Dump(j)
        WriteOutFile(p)
        ;ToolTip %p%.%outputFile%,0,0
        ;out.Close()
        }
    }
    }
    sleep,%FrequencyTimeout%
}


#Include %A_LineFile%\..\hotkey.ahk