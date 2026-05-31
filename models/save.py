def _save(self):
    if not self._album_data or not self._cover_image:
        messagebox.showwarning("Boş", "Önce albüm oluşturun.")
        return
    folder = filedialog.askdirectory(title="Kayıt Klasörü Seç")
    if not folder:
        return
    name = self._album_data.get("album_name", "album").replace(" ", "_")
    json_path = os.path.join(folder, f"{name}.json")
    png_path  = os.path.join(folder, f"{name}_cover.png")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(self._album_data, f, ensure_ascii=False, indent=2)
    self._cover_image.save(png_path, "PNG")
    messagebox.showinfo("Kaydedildi!", f"{json_path}\n{png_path}")
