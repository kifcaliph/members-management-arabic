SetCompressor lzma

; Modern UI installer stuff
  !include "MUI2.nsh"
  !define MUI_ABORTWARNING
  !include nsDialogs.nsh
  !include FileFunc.nsh
 
;======================================================
; Installer Information
 
  Name "Club Members Pro 1.0.1"
  OutFile "ClubMembers_setup_1.0.1.exe"
  InstallDir C:\App
  
;======================================================
; Pages
 
  !insertmacro MUI_PAGE_DIRECTORY
  !insertmacro MUI_PAGE_INSTFILES
  !insertmacro MUI_PAGE_FINISH
  !insertmacro MUI_LANGUAGE "English"
  
  !Macro "CreateURL" "URLFile" "URLSite" "URLDesc"
  WriteINIStr "$EXEDIR\${URLFile}.URL" "InternetShortcut" "URL" "${URLSite}"
  SetShellVarContext "all"
  CreateShortCut "$DESKTOP\${URLFile}.lnk" "$EXEDIR\${URLFile}.url" "" "$EXEDIR\makeURL.exe" 0 "SW_SHOWNORMAL" "" "${URLDesc}"
  !macroend
  
;--------------------------------
; Uninstaller pages
  !insertmacro MUI_UNPAGE_CONFIRM
  !insertmacro MUI_UNPAGE_INSTFILES
  !insertmacro MUI_UNPAGE_FINISH
 

;======================================================
; These are the programs that are needed by.
Var DataFilePath
Section "Files" SecInstall
  SetOutPath $INSTDIR\Prerequisites
  MessageBox MB_YESNO "Install Python 2.7.2" /SD IDYES IDNO endActiveSync
    File "C:\Users\kifcaliph\Desktop\python-2.7.2.msi"
    ExecWait 'msiexec /i "$INSTDIR\Prerequisites\python-2.7.2.msi"/qb ALLUSERS=1'
	
	SetOutPath "$INSTDIR"
	File /r "$Desktop\web2py\"
	SetOutPath "$INSTDIR\applications"
	nsDialogs::SelectFileDialog open $DESKTOP "W2P files|*.w2p"
	Pop $0
	${GetBaseName} $0 $1
	${IfNot} ${FileExists} $0
	    MessageBox mb_iconstop "You must locate the database"
        Abort
	${Else}
	    untgz::extract "-d" "$INSTDIR\applications\$1" "$0"
	${EndIf}
	SetOutPath $INSTDIR\Prerequisites
	File "$Desktop\nssm\nss\win32\nssm.exe"
	ExecWait '$INSTDIR\Prerequisites\nssm.exe install ClubMembers "C:\Python27\python.exe" "$INSTDIR\web2py.py -p 8071 -i 0.0.0.0 --password=123"'
	!insertmacro "CreateURL" "Club Member Pro" "http://127.0.0.1:8071/$1/default/index" "Members App"
    Goto endActiveSync
  endActiveSync:
SectionEnd

 Section "Uninstall"
	RMDir "$INSTDIR"
SectionEnd

