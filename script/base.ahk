EnvGet,FrequencyTimeout ,FrequencyTimeout
if(!FrequencyTimeout){
FrequencyTimeout:=400
}
EnvGet,inputFilePath ,IO_INPUT_FILE
EnvGet,outputFilePath ,IO_OUTPUT_FILE

inputFile:=FileOpen(inputFilePath, "r")
outputFile:=FileOpen(outputFilePath, "w")
p:=inputFilePath
WriteOutFile(msg){
global outputFile
outputFile.Write(msg)
 outputFile.Write("`n")
 outputFile.Read(0)
}
