Configuration MyDSCDemo
{
   Import-DSCResource -Module nx
   Node "192.168.1.62"{    
        nxFile myTestFile
        {
            Ensure = "Present" 
            Type = "File"
            DestinationPath = "/tmp/dsctest"   
            Contents="This is my DSC Test!"
        }
    }
}
 