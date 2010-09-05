; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

[Setup]
; NOTE: The value of AppId uniquely identifies this application.
; Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{8154F675-986F-4E74-AF85-E6432F344F1D}
AppName=PythonCad
AppVerName=PythonCad Alfa R38 
AppPublisher=Matteo Boscolo OpenSource
AppPublisherURL=http://sourceforge.net/projects/pythoncad/
AppSupportURL=http://sourceforge.net/projects/pythoncad/
AppUpdatesURL=http://sourceforge.net/projects/pythoncad/
DefaultDirName={pf}\PythonCad
DefaultGroupName=PythonCad
OutputBaseFilename=setup
SetupIconFile=C:\Users\mboscolo\Desktop\R38\pythoncad\PythonCAD\icons\pythoncad.ico
Compression=lzma
SolidCompression=yes

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "german"; MessagesFile: "compiler:Languages\German.isl"
Name: "italian"; MessagesFile: "compiler:Languages\Italian.isl"
Name: "portuguese"; MessagesFile: "compiler:Languages\Portuguese.isl"
Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "C:\Users\mboscolo\Desktop\R38\trunk\pythoncad_qt\dist\pythoncad_qt\pythoncad_qt.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\mboscolo\Desktop\R38\trunk\pythoncad_qt\dist\pythoncad_qt\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "C:\Users\mboscolo\Desktop\R38\pythoncad\PythonCAD\icons\*"; DestDir: "{app}\icons"; Flags: ignoreversion recursesubdirs createallsubdirs
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{group}\PythonCad"; Filename: "{app}\pythoncad_qt.exe";WorkingDir: "{app}"
Name: "{commondesktop}\PythonCad"; Filename: "{app}\pythoncad_qt.exe"; Tasks: desktopicon ;WorkingDir: "{app}"
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\PythonCad"; Filename: "{app}\pythoncad_qt.exe"; Tasks: quicklaunchicon  ;WorkingDir: "{app}"

[Run]
Filename: "{app}\pythoncad_qt.exe"; Description: "{cm:LaunchProgram,PythonCad}"; Flags: nowait postinstall skipifsilent

