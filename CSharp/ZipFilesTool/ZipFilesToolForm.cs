using ICSharpCode.SharpZipLib.Zip;
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace ZipFilesTool
{
    public partial class ZipFilesToolFrom : Form
    {
        public ZipFilesToolFrom()
        {
            InitializeComponent();
            this.AllowDrop = true;
            this.DragDrop += new DragEventHandler(this.ZipFilesToolFrom_DragDrop);
            this.DragEnter += new DragEventHandler(this.ZipFilesToolFrom_DragEnter);
        }

        private void ZipFilesToolFrom_DragEnter(object sender, DragEventArgs e)
        {
            e.Effect = DragDropEffects.Move;
        }
        
        private void ZipFilesToolFrom_DragDrop(object sender, DragEventArgs e)
        {
            string path = ((System.Array)e.Data.GetData(DataFormats.FileDrop)).GetValue(0).ToString();
            result_label.Text = path + "\n";
            ZipFiles(path);
        }
        
        private void ZipFiles(string path)
        {
            if (!Directory.Exists(path))
                return;

            string resultPath = path + "_gplay";
            if (Directory.Exists(resultPath))
                Directory.Delete(resultPath, true);
            Directory.CreateDirectory(resultPath);

            string[] files = Directory.GetFiles(path, "*", SearchOption.AllDirectories);

            try
            {
                foreach(string file in files)
                {
                    string zipFilePath = file.Replace(path, resultPath) + ".obb";
                    string fileName = Path.GetFileName(file);

                    string zipFileDir = Path.GetDirectoryName(zipFilePath);
                    if (!Directory.Exists(zipFileDir))
                        Directory.CreateDirectory(zipFileDir);

                    using (ZipOutputStream zipOutputStream = new ZipOutputStream(File.Open(zipFilePath, FileMode.OpenOrCreate)))
                    {
                        zipOutputStream.SetLevel(8);
                        zipOutputStream.UseZip64 = UseZip64.Off;
                        ZipEntry zipEntry = new ZipEntry(fileName);
                        zipOutputStream.PutNextEntry(zipEntry);

                        using (FileStream fileStream = File.Open(file, FileMode.Open))
                        {
                            PipeStream(fileStream, zipOutputStream);
                        }
                        zipOutputStream.Finish();
                        zipOutputStream.Close();
                    }

                    result_label.Text += zipFilePath + "\n";
                }
            }
            catch (Exception e)
            {
                result_label.Text = e.ToString();
            }
        }

        private void PipeStream(Stream inputStream, Stream outputStream)
        {
            if (inputStream == null || outputStream == null)
                return;

            byte[] buffer = new byte[2048];
            int sizeRead = 0;
            while (true)
            {
                sizeRead = inputStream.Read(buffer, 0, buffer.Length);
                if (sizeRead > 0)
                    outputStream.Write(buffer, 0, sizeRead);
                else
                    break;
            }
        }

        //private void ZipStreamToObb(Stream inputStream, string zipFilePath, string entryName)
        //{
        //    if (inputStream == null)
        //        return;

        //    using (FileStream fileStream = File.Open(zipFilePath, FileMode.OpenOrCreate))
        //    {
        //        using (ZipOutputStream zipOutputStream = new ZipOutputStream(fileStream))
        //        {
        //            zipOutputStream.UseZip64 = UseZip64.Off;
        //            ZipEntry zipEntry = new ZipEntry(entryName);

        //            zipOutputStream.PutNextEntry(zipEntry);
        //            zipOutputStream.SetLevel(8);

        //            PipeStream(inputStream, zipOutputStream);

        //            zipOutputStream.Finish();
        //            zipOutputStream.Close();
        //        }
        //    }
        //}
    }
}
