ifeq ($(OS),Windows_NT)
    DELETE := cmd /C rd /s /q
else
    DELETE := rm -rf
endif

clean:
	@$(DELETE) dist build
	@$(DELETE) *.spec

interpreter:
	@pyinstaller --onefile --windowed --icon="icon.ico" src/interpreter.py --name="brainfucker.py.exe" --clean
	@$(DELETE) *.spec
