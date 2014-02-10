import java.net.*;
import javax.net.ssl.*;
import java.security.*;
import java.security.cert.*;

public class TrustModifier {
    private static final TrustingHostnameVerifier HOSTNAME_VERIFIER = new TrustingHostnameVerifier();
    private static SSLSocketFactory factory;

    public static void relaxHostChecking(HttpURLConnection connection)
                    throws Exception {
        
        if(connection instanceof HttpsURLConnection){
                HttpsURLConnection secureConnection = (HttpsURLConnection)connection;
                SSLSocketFactory sslFactory = prepFactory(secureConnection);
                secureConnection.setSSLSocketFactory(sslFactory);
                secureConnection.setHostnameVerifier(HOSTNAME_VERIFIER);
        }
    }

    static synchronized SSLSocketFactory prepFactory(HttpsURLConnection secureConnection)
                    throws Exception {

        if(factory == null){
                SSLContext ctx = SSLContext.getInstance("TLS");
                ctx.init(null, new TrustManager[]{new AlwaysTrustManager() }, null);
                factory = ctx.getSocketFactory();
        }
        return factory;
    }

    private static final class TrustingHostnameVerifier implements HostnameVerifier {
        public boolean verify(String hostname, SSLSession session){
                return true;
        }
    }

    private static class AlwaysTrustManager implements X509TrustManager {
        public void checkClientTrusted(X509Certificate[] arg0, String arg1){}
        public void checkServerTrusted(X509Certificate[] arg0, String arg1){}
        public X509Certificate[] getAcceptedIssuers() { return null; }
    }
}
