package org.melwyn.mobileauthpoc;

import android.hardware.fingerprint.FingerprintManager;
import android.os.AsyncTask;
import android.os.CancellationSignal;
import android.util.JsonReader;
import android.widget.TextView;

import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;

/**
 * Created by francesco on 29/11/16.
 */

public class FingerprintHandler extends FingerprintManager.AuthenticationCallback {

    private TextView tv;


    public FingerprintHandler(TextView tv) {
        this.tv = tv;
    }

    @Override
    public void onAuthenticationError(int errorCode, CharSequence errString) {
        super.onAuthenticationError(errorCode, errString);
        tv.setText("Auth error");
    }

    @Override
    public void onAuthenticationHelp(int helpCode, CharSequence helpString) {
        super.onAuthenticationHelp(helpCode, helpString);

    }

    @Override
    public void onAuthenticationSucceeded(FingerprintManager.AuthenticationResult result) {
        super.onAuthenticationSucceeded(result);
        AsyncTask.execute(new Runnable() {
            @Override
            public void run() {
                PostDataAPI();
            }
        });
    }

    @Override
    public void onAuthenticationFailed() {
        super.onAuthenticationFailed();
    }

    public void doAuth(FingerprintManager manager, FingerprintManager.CryptoObject obj) {
        CancellationSignal signal = new CancellationSignal();

        try {
            manager.authenticate(obj, signal, 0, this, null);
        }
        catch(SecurityException sce) {}
    }

    private void PostDataAPI(){
        try {
            URL httpbinEndpoint = new URL("http://192.168.43.236/api/authenticate");
            HttpURLConnection myConnection = (HttpURLConnection) httpbinEndpoint.openConnection();
            myConnection.setRequestMethod("POST");
            myConnection.setRequestProperty("Content-Type","application/json");
            JSONObject obj = new JSONObject();
            obj.put("text","Melwyn");
            myConnection.setDoOutput(true);
            myConnection.getOutputStream().write(obj.toString().getBytes());
            BufferedReader br = new BufferedReader(new InputStreamReader(myConnection.getInputStream()));
            String s;
            String output = "";
            while((s = br.readLine()) != null)
            {
                output += s;
            }
            JSONObject resobj = new JSONObject(output);
            output = resobj.getString("Message");
            System.out.println(resobj.getString("Message"));
            myConnection.disconnect();
            tv.setText(output);
            tv.setTextColor(tv.getContext().getResources().getColor(android.R.color.holo_green_light));
        }
        catch(Exception ex) {
            // don't do anything for now
            System.out.println(ex.getMessage());
        }
    }
}
