source config.env &&
mkdir -p exe/macos &&
pyinstaller --noconfirm --windowed --onedir --noconsole --add-data "${CUSTOMTKINTER_PATH}:customtkinter/" src/dbf-to-csv.py &&
rsync -a dist/dbf-to-csv.app exe/macos &&
rm dbf-to-csv.spec &&
rm -r build &&
rm -r dist
