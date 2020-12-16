#Include %A_LineFile%\..\JSON.ahk

HotKeyIt(keys){
  j:={keys:keys}
 out:=FileOpen("./output_hotkey", "w")

 p:=JSON.Dump(j)
 out.Write(p)
 out.Close()
}


#^p::Pause

F2::
{
MouseMove, 20, 30, 50, R
return
}