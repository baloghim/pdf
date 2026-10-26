using System;
using System.Collections.Generic;
using System.Drawing;
using System.IO;
using System.Windows.Forms;
using PdfSharp.Pdf;
using PdfSharp.Pdf.IO;

namespace PdfMuhelyXP
{
    static class PdfOperations
    {
        public static void CheckOutput(string path, params string[] inputs)
        {
            if (File.Exists(path)) throw new IOException("A kimeneti fájl már létezik. Válassz új nevet.");
            foreach (string input in inputs)
                if (String.Equals(Path.GetFullPath(input), Path.GetFullPath(path), StringComparison.OrdinalIgnoreCase))
                    throw new IOException("A bemeneti PDF nem írható felül.");
        }
        public static void Save(PdfDocument document, string path)
        {
            string temp = Path.Combine(Path.GetDirectoryName(Path.GetFullPath(path)), Guid.NewGuid() + ".tmp");
            try { document.Save(temp); File.Move(temp, path); }
            finally { if (File.Exists(temp)) File.Delete(temp); }
        }
        public static void Merge(string[] paths, string output)
        {
            if (paths.Length < 2) throw new ArgumentException("Legalább két PDF szükséges.");
            CheckOutput(output, paths);
            using (PdfDocument target = new PdfDocument())
            {
                foreach (string path in paths)
                    using (PdfDocument source = PdfReader.Open(path, PdfDocumentOpenMode.Import))
                        for (int i = 0; i < source.PageCount; i++) target.AddPage(source.Pages[i]);
                Save(target, output);
            }
        }
        public static void Split(string source, int cut, string first, string second)
        {
            CheckOutput(first, source); CheckOutput(second, source);
            if (String.Equals(Path.GetFullPath(first), Path.GetFullPath(second), StringComparison.OrdinalIgnoreCase))
                throw new ArgumentException("A két kimenet neve legyen különböző.");
            using (PdfDocument input = PdfReader.Open(source, PdfDocumentOpenMode.Import))
            using (PdfDocument a = new PdfDocument())
            using (PdfDocument b = new PdfDocument())
            {
                if (cut < 1 || cut >= input.PageCount) throw new ArgumentException("Érvénytelen vágási pont.");
                for (int i = 0; i < input.PageCount; i++)
                    (i < cut ? a : b).AddPage(input.Pages[i]);
                Save(a, first);
                try { Save(b, second); }
                catch { File.Delete(first); throw; }
            }
        }
    }

    sealed class MainWindow : Form
    {
        readonly TabControl tabs = new TabControl();
        readonly ListBox files = new ListBox();
        readonly Label sourceLabel = new Label();
        readonly NumericUpDown cut = new NumericUpDown();
        string source;
        public MainWindow()
        {
            Text = "PDF Műhely – Windows XP x86";
            ClientSize = new Size(680, 440);
            MinimumSize = new Size(620, 450);
            tabs.Dock = DockStyle.Fill;
            Controls.Add(tabs);
            var merge = new TabPage("Összefűzés");
            var split = new TabPage("Kettévágás");
            tabs.TabPages.Add(merge); tabs.TabPages.Add(split);
            files.SetBounds(16, 44, 610, 230);
            files.Anchor = AnchorStyles.Top | AnchorStyles.Bottom | AnchorStyles.Left | AnchorStyles.Right;
            files.SelectionMode = SelectionMode.MultiExtended;
            merge.Controls.Add(files);
            var hint = new Label { Text = "Húzz ide PDF-eket. A sorrend a Fel / Le gombokkal módosítható.", AutoSize = true, Left = 16, Top = 16 };
            merge.Controls.Add(hint);
            AddButton(merge, "PDF-ek hozzáadása…", 16, 290, delegate {
                using (var dialog = new OpenFileDialog { Filter = "PDF|*.pdf", Multiselect = true })
                    if (dialog.ShowDialog() == DialogResult.OK) files.Items.AddRange(dialog.FileNames);
            });
            AddButton(merge, "Eltávolítás", 210, 290, delegate {
                while (files.SelectedIndices.Count > 0) files.Items.RemoveAt(files.SelectedIndices[0]);
            });
            AddButton(merge, "Fel", 404, 290, delegate { MoveSelected(-1); });
            AddButton(merge, "Le", 404, 330, delegate { MoveSelected(1); });
            AddButton(merge, "Összefűzés és mentés…", 16, 330, delegate {
                string target = Destination("Összefűzött PDF", "osszefuzott.pdf");
                if (target == null) return;
                var paths = new List<string>(); foreach (string p in files.Items) paths.Add(p);
                PdfOperations.Merge(paths.ToArray(), target); Done();
            });
            sourceLabel.SetBounds(16, 70, 610, 60);
            sourceLabel.Text = "Húzz ide egy PDF-et, vagy válaszd ki a gombbal.";
            split.Controls.Add(sourceLabel);
            AddButton(split, "PDF kiválasztása…", 16, 16, delegate {
                using (var dialog = new OpenFileDialog { Filter = "PDF|*.pdf" })
                    if (dialog.ShowDialog() == DialogResult.OK) OpenSource(dialog.FileName);
            });
            split.Controls.Add(new Label { Text = "Az első rész utolsó oldalának száma:", AutoSize = true, Left = 16, Top = 146 });
            cut.SetBounds(16, 176, 120, 28); cut.Minimum = 1; cut.Enabled = false;
            split.Controls.Add(cut);
            AddButton(split, "Kettévágás és mentés…", 16, 230, delegate {
                if (source == null) throw new ArgumentException("Először válassz PDF-et.");
                string a = Destination("Első rész", Path.GetFileNameWithoutExtension(source) + "_1.pdf");
                if (a == null) return;
                string b = Destination("Második rész", Path.GetFileNameWithoutExtension(source) + "_2.pdf");
                if (b == null) return;
                PdfOperations.Split(source, (int)cut.Value, a, b); Done();
            });
            EnableDrop(this);
        }
        void AddButton(Control parent, string text, int x, int y, Action action)
        {
            var button = new Button { Text = text, Left = x, Top = y, Width = 184, Height = 34 };
            button.Click += delegate { Guard(action); }; parent.Controls.Add(button);
        }
        void MoveSelected(int direction)
        {
            if (files.SelectedIndices.Count != 1) return;
            int i = files.SelectedIndex, j = i + direction;
            if (j < 0 || j >= files.Items.Count) return;
            object item = files.Items[i]; files.Items.RemoveAt(i); files.Items.Insert(j, item); files.SelectedIndex = j;
        }
        void EnableDrop(Control control)
        {
            control.AllowDrop = true;
            control.DragEnter += delegate(object sender, DragEventArgs e) {
                e.Effect = ValidDrop(e) ? DragDropEffects.Copy : DragDropEffects.None;
            };
            control.DragDrop += delegate(object sender, DragEventArgs e) {
                Guard(delegate {
                    if (!ValidDrop(e)) return;
                    string[] paths = (string[])e.Data.GetData(DataFormats.FileDrop);
                    if (tabs.SelectedIndex == 0) files.Items.AddRange(paths); else OpenSource(paths[0]);
                });
            };
            foreach (Control child in control.Controls) EnableDrop(child);
        }
        bool ValidDrop(DragEventArgs e)
        {
            if (!e.Data.GetDataPresent(DataFormats.FileDrop)) return false;
            string[] paths = (string[])e.Data.GetData(DataFormats.FileDrop);
            if (paths.Length == 0 || (tabs.SelectedIndex == 1 && paths.Length != 1)) return false;
            foreach (string path in paths)
                if (!File.Exists(path) || !String.Equals(Path.GetExtension(path), ".pdf", StringComparison.OrdinalIgnoreCase)) return false;
            return true;
        }
        void OpenSource(string path)
        {
            using (var pdf = PdfReader.Open(path, PdfDocumentOpenMode.Import))
            {
                if (pdf.PageCount < 2) throw new ArgumentException("Legalább két oldal szükséges.");
                cut.Value = 1; cut.Maximum = pdf.PageCount - 1; cut.Enabled = true;
                source = path; sourceLabel.Text = Path.GetFileName(path) + " – " + pdf.PageCount + " oldal";
            }
        }
        static string Destination(string title, string name)
        {
            using (var dialog = new SaveFileDialog { Title = title, Filter = "PDF|*.pdf", FileName = name, DefaultExt = "pdf", AddExtension = true })
                return dialog.ShowDialog() == DialogResult.OK ? dialog.FileName : null;
        }
        static void Done() { MessageBox.Show("A PDF-fájlok mentve.", "Elkészült"); }
        static void Guard(Action action)
        {
            try { action(); } catch (Exception e) { MessageBox.Show(e.Message, "Nem sikerült a művelet", MessageBoxButtons.OK, MessageBoxIcon.Warning); }
        }
    }

    static class Program
    {
        [STAThread]
        static int Main(string[] args)
        {
            try
            {
                if (args.Length > 0 && args[0] == "--self-test") { SelfTest(); return 0; }
                Application.EnableVisualStyles();
                Application.SetCompatibleTextRenderingDefault(false);
                if (args.Length > 0 && args[0] == "--smoke-test")
                    using (var window = new MainWindow()) { window.Show(); Application.DoEvents(); return 0; }
                Application.Run(new MainWindow()); return 0;
            }
            catch (Exception e) { Console.Error.WriteLine(e); return 1; }
        }
        static void Assert(bool condition) { if (!condition) throw new Exception("Self-test failed"); }
        static void SelfTest()
        {
            string dir = Path.Combine(Path.GetTempPath(), "pdf-xp-" + Guid.NewGuid()); Directory.CreateDirectory(dir);
            try
            {
                string a = Path.Combine(dir, "a.pdf"), b = Path.Combine(dir, "b.pdf"), merged = Path.Combine(dir, "merged.pdf");
                using (var doc = new PdfDocument()) { doc.AddPage().Width = 200; doc.AddPage().Width = 300; doc.Save(a); }
                using (var doc = new PdfDocument()) { doc.AddPage().Width = 400; doc.Save(b); }
                PdfOperations.Merge(new string[] { b, a }, merged);
                using (var doc = PdfReader.Open(merged, PdfDocumentOpenMode.Import)) {
                    Assert(doc.PageCount == 3); Assert(doc.Pages[0].Width.Point == 400); Assert(doc.Pages[2].Width.Point == 300);
                }
                string first = Path.Combine(dir, "first.pdf"), second = Path.Combine(dir, "second.pdf");
                PdfOperations.Split(merged, 1, first, second);
                using (var doc = PdfReader.Open(first, PdfDocumentOpenMode.Import)) Assert(doc.PageCount == 1);
                using (var doc = PdfReader.Open(second, PdfDocumentOpenMode.Import)) Assert(doc.PageCount == 2);
                bool refused = false;
                try { PdfOperations.Merge(new string[] { a, b }, a); } catch (IOException) { refused = true; }
                Assert(refused);
                refused = false;
                try { PdfOperations.Split(merged, 0, Path.Combine(dir, "bad1.pdf"), Path.Combine(dir, "bad2.pdf")); } catch (ArgumentException) { refused = true; }
                Assert(refused); Assert(!File.Exists(Path.Combine(dir, "bad1.pdf")));
            }
            finally { Directory.Delete(dir, true); }
        }
    }
}
