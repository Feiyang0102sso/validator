@echo off
echo �������� mock_dataset �����в��������ļ��кͷ� .md �ļ����������棩...

REM ����ɾ�� mock_dataset �³� .md ����������ļ���
for /d %%i in (mock_dataset\*) do (
    echo ɾ���ļ��У�%%i
    rmdir /s /q "%%i"
)

REM ����ɾ�� mock_dataset �³� .md ������е��ļ�
for %%f in (mock_dataset\*) do (
    if /I not "%%~xf"==".md" (
        echo ɾ���ļ���%%f
        del /f /q "%%f"
    )
)

echo ������� ?
pause
