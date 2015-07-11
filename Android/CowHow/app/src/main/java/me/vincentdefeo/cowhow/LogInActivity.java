package me.vincentdefeo.cowhow;

import android.app.AlertDialog;
import android.content.Intent;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.EditText;

import me.vincentdefeo.cowhow.utils.Preferences;


public class LogInActivity extends AppCompatActivity {

    private static final String TOKEN_KEY = "KEY_TOKEN";
    private static final String TAG = "LoginActivity";

    public static final String AUTH_TOKEN_TYPE = "standard";

    EditText nameField, pwdField;
    private String mail = "", pwd = "";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_log_in);

        String userAuth = checkForLocalAuth();

        if (isValidAuth(userAuth)) {
            goToApp();
            return;
        }

        nameField = (EditText) findViewById(R.id.login_mail);
        pwdField = (EditText) findViewById(R.id.login_pwd);


        findViewById(R.id.login_btn)
                .setOnClickListener(new View.OnClickListener() {
                    @Override
                    public void onClick(View v) {
                        if (validateFields()) {
                            saveUserAuth();
                            goToApp();
                        }
                    }
                });
    }

    private void goToApp()
    {
        startActivity(new Intent(this, MainActivity.class));
    }

    private boolean isValidAuth(String auth)
    {
        return auth != null && !auth.equals("") && !auth.equalsIgnoreCase(":");
    }

    private String checkForLocalAuth()
    { return Preferences.getUserAuth(this);}

    private boolean validateFields() {
        boolean valid = false;

        try {
            mail = nameField.getText().toString();
        } catch (Exception e) {
            displayInvalidData();
        }

        try {
            pwd = pwdField.getText().toString();
        } catch (Exception e) {
            displayInvalidData();
        }

        if (mail != "" && mail != null)
            if (pwd != "" && pwd != null)
                valid = true;

        return valid;
    }

    private void displayInvalidData()
    {
        new AlertDialog.Builder(this)
                .setTitle("Invalid data")
                .setMessage("Check your input please")
                .create()
                .show();
    }

    private void saveUserAuth()
    {
        Preferences.saveUser(this, mail, pwd);
    }
}
