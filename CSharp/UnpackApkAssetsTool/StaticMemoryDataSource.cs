using System;
using System.IO;
using ICSharpCode.SharpZipLib.Zip;


namespace UnpackApkAssetsTool
{
    public class StaticMemoryDataSource : IStaticDataSource
    {
        private MemoryStream stream;

        public StaticMemoryDataSource(string str)
        {
            var bytes = System.Text.Encoding.UTF8.GetBytes(str);
            stream = new MemoryStream(bytes);
        }

        ~StaticMemoryDataSource()
        {
            stream.Close();
        }

        public StaticMemoryDataSource(int number)
        {
            var bytes = BitConverter.GetBytes(number);
            stream = new MemoryStream(bytes);
        }

        #region IDataSource Members
        public Stream GetSource()
        {
            return stream;
        }
        #endregion
    }
}
