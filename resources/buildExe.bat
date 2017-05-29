cd ..\..\PeakStrainer
C:\apps\Anaconda2\Scripts\pyinstaller.exe peakStrainer.spec
git rev-parse HEAD > dist\peakStrainerApp\gitHEAD.txt
#
cd dist
"C:\Program Files\7-Zip\7z.exe" u peakStrainerApp.zip peakStrainerApp 
 rmdir /s /q peakStrainerApp
 cd ..
 rmdir /s /q build