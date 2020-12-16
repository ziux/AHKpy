#Include %A_LineFile%\..\JSON.ahk
#Include %A_LineFile%\..\base.ahk

HotKeyIt(keys){
 j:={keys:keys}
 p:=JSON.Dump(j)

 WriteOutFile(p)
}


#^p::Pause

