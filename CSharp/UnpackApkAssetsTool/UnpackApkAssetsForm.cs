using ICSharpCode.SharpZipLib.Core;
using ICSharpCode.SharpZipLib.Zip;
using System;
using System.Collections.Generic;
using System.IO;
using System.Text.RegularExpressions;
using System.Windows.Forms;

namespace UnpackApkAssetsTool
{
    public partial class UnpackApkAssetsForm : Form
    {
        public UnpackApkAssetsForm()
        {
            InitializeComponent();
            this.AllowDrop = true;
            this.DragDrop += new DragEventHandler(this.UnpackApkAssetsForm_DragDrop);
            this.DragEnter += new DragEventHandler(this.UnpackApkAssetsForm_DragEnter);
        }

        private void UnpackApkAssetsForm_DragEnter(object sender, DragEventArgs e)
        {
            e.Effect = DragDropEffects.Move;
        }


        private void UnpackApkAssetsForm_DragDrop(object sender, DragEventArgs e)
        {
            string path = ((System.Array)e.Data.GetData(DataFormats.FileDrop)).GetValue(0).ToString();

            //MessageBox.Show(path);
            UnpackApkAssets(path);
        }


        private void UnpackApkAssets(string apkPath)
        {
            if (!File.Exists(apkPath))
                return;

            string destDirRoot = Path.GetDirectoryName(apkPath);
            destDirRoot += "/" + Path.GetFileNameWithoutExtension(apkPath) + "_gplay/";
            if (Directory.Exists(destDirRoot))
                Directory.Delete(destDirRoot, true);
            Directory.CreateDirectory(destDirRoot);

            try
            {
                List<string> lstSplit0Files = new List<string>();
                using (ZipInputStream zipInputStream = new ZipInputStream(File.OpenRead(apkPath)))
                {
                    ZipEntry theEntry;
                    label_result.Text = string.Empty;

                    //List<string> lstMergeFilePaths = new List<string>();
                    while ((theEntry = zipInputStream.GetNextEntry()) != null)
                    {
                        string filePath = theEntry.Name;

                        if (!filePath.StartsWith("assets/"))
                            continue;

                        string relativeDirName = Path.GetDirectoryName(filePath);
                        string fileName = Path.GetFileName(filePath);

                        string fileDir = destDirRoot + relativeDirName + "/";

                        if (!Directory.Exists(fileDir))
                            Directory.CreateDirectory(fileDir);

                        bool isNeedZip = false;
                        string destFileName = fileName;

                        Regex regex = new Regex(".split0$");
                        if (regex.IsMatch(destFileName))
                        {
                            lstSplit0Files.Add(filePath);
                            //destFileName = regex.Replace(destFileName, "");
                            //string mergeFilePath = fileDir + destFileName;
                            //if (!lstMergeFilePaths.Contains(mergeFilePath))
                            //    lstMergeFilePaths.Add(mergeFilePath);
                        }
                        //else
                        if (relativeDirName != "assets" && !filePath.Equals("assets/bin/Data/settings.xml", StringComparison.OrdinalIgnoreCase))
                        {
                            isNeedZip = true;
                            destFileName += ".obb";
                        }

                        if (isNeedZip)
                        {
                            ZipStreamToObb(zipInputStream, fileDir + destFileName, fileName);
                        }
                        else
                        {
                            using (FileStream fileStream = File.Open(fileDir + destFileName, FileMode.OpenOrCreate))
                            {
                                fileStream.Seek(0, SeekOrigin.End);
                                PipeStream(zipInputStream, fileStream);
                            }
                        }
                    }

                    //foreach (string mergeFilePath in lstMergeFilePaths)
                    //{
                    //    string zipMergeFilePath = mergeFilePath + ".obb";
                    //    using (FileStream fileStream = File.Open(mergeFilePath, FileMode.Open))
                    //    {
                    //        ZipStreamToObb(fileStream, zipMergeFilePath, Path.GetFileName(mergeFilePath));
                    //    }
                    //    File.Delete(mergeFilePath);
                    //}
                }
                AddSplit0InGlobalPackage(destDirRoot, lstSplit0Files);
            }
            catch (Exception e)
            {
                label_result.Text = e.ToString();
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

        private void ZipStreamToObb(Stream inputStream, string zipFilePath, string entryName)
        {
            if (inputStream == null)
                return;

            using (FileStream fileStream = File.Open(zipFilePath, FileMode.OpenOrCreate))
            {
                using (ZipOutputStream zipOutputStream = new ZipOutputStream(fileStream))
                {
                    zipOutputStream.UseZip64 = UseZip64.Off;
                    ZipEntry zipEntry = new ZipEntry(entryName);

                    zipOutputStream.PutNextEntry(zipEntry);
                    zipOutputStream.SetLevel(8);

                    PipeStream(inputStream, zipOutputStream);

                    zipOutputStream.Finish();
                    zipOutputStream.Close();
                }
            }
        }

        private void AddSplit0InGlobalPackage(string destDirRoot, List<string> lstSplit0Files)
        {
            string globalPackagePath = destDirRoot + "assets/bin/Data/globalgamemanagers.obb";
            if(!File.Exists(globalPackagePath))
            {
                label_result.Text = "globalPackagePath not exists";
                return;
            }
            
            using (ZipFile zipFile = new ZipFile(File.Open(globalPackagePath, FileMode.Open)))
            {
                zipFile.BeginUpdate();
                for (int i = 0; i < lstSplit0Files.Count; ++i)
                {
                    string entryName = lstSplit0Files[i];
                    zipFile.Add(new StaticMemoryDataSource(i), entryName);
                }
                zipFile.CommitUpdate();
            }
        }
    }
}
