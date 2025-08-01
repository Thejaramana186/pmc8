# Email Setup Instructions for PI Management System

## Supported Email Providers

The PI Management System supports all major email providers. Here are the most common configurations:

## 1. Gmail Setup (Recommended)

### Step 1: Enable 2-Factor Authentication
1. Go to your Google Account settings
2. Navigate to Security
3. Enable 2-Step Verification

### Step 2: Generate App Password
1. Go to https://myaccount.google.com/apppasswords
2. Select "Mail" as the app
3. Select "Other" as the device and name it "PI Management System"
4. Copy the 16-character app password (it will look like: `abcd efgh ijkl mnop`)

### Step 3: Update .env File
```env
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USE_SSL=false
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=abcd efgh ijkl mnop
MAIL_DEFAULT_SENDER=your-email@gmail.com
```

**Important**: Use the App Password (16 characters with spaces), NOT your regular Gmail password!

---

## 2. Yahoo Mail Setup

### Step 1: Enable App Passwords
1. Go to Yahoo Account Security: https://login.yahoo.com/account/security
2. Turn on 2-step verification if not already enabled
3. Generate an app password for "Mail"

### Step 2: Update .env File
```env
MAIL_SERVER=smtp.mail.yahoo.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USE_SSL=false
MAIL_USERNAME=your-email@yahoo.com
MAIL_PASSWORD=your-app-password
MAIL_DEFAULT_SENDER=your-email@yahoo.com
```

**Alternative Yahoo Configuration (SSL):**
```env
MAIL_SERVER=smtp.mail.yahoo.com
MAIL_PORT=465
MAIL_USE_TLS=false
MAIL_USE_SSL=true
MAIL_USERNAME=your-email@yahoo.com
MAIL_PASSWORD=your-app-password
MAIL_DEFAULT_SENDER=your-email@yahoo.com
```

---

## 3. Outlook/Hotmail Setup

### Step 1: Enable App Passwords (if 2FA is enabled)
1. Go to Microsoft Account Security: https://account.microsoft.com/security
2. If you have 2-step verification enabled, create an app password
3. If 2FA is not enabled, you can use your regular password

### Step 2: Update .env File
```env
MAIL_SERVER=smtp-mail.outlook.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USE_SSL=false
MAIL_USERNAME=your-email@outlook.com
MAIL_PASSWORD=your-password-or-app-password
MAIL_DEFAULT_SENDER=your-email@outlook.com
```

**Alternative Outlook Configuration (SSL):**
```env
MAIL_SERVER=smtp-mail.outlook.com
MAIL_PORT=465
MAIL_USE_TLS=false
MAIL_USE_SSL=true
MAIL_USERNAME=your-email@outlook.com
MAIL_PASSWORD=your-password-or-app-password
MAIL_DEFAULT_SENDER=your-email@outlook.com
```

---

## 4. Other Email Providers

### iCloud Mail
```env
MAIL_SERVER=smtp.mail.me.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USE_SSL=false
MAIL_USERNAME=your-email@icloud.com
MAIL_PASSWORD=your-app-specific-password
MAIL_DEFAULT_SENDER=your-email@icloud.com
```

### Zoho Mail
```env
MAIL_SERVER=smtp.zoho.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USE_SSL=false
MAIL_USERNAME=your-email@zoho.com
MAIL_PASSWORD=your-password
MAIL_DEFAULT_SENDER=your-email@zoho.com
```

### Custom SMTP Server
```env
MAIL_SERVER=your-smtp-server.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USE_SSL=false
MAIL_USERNAME=your-username
MAIL_PASSWORD=your-password
MAIL_DEFAULT_SENDER=your-email@yourdomain.com
```

---

## Configuration Notes

### Port and Security Settings:
- **Port 587**: Use with `MAIL_USE_TLS=true` and `MAIL_USE_SSL=false`
- **Port 465**: Use with `MAIL_USE_TLS=false` and `MAIL_USE_SSL=true`
- **Port 25**: Usually for local/internal servers (not recommended for external providers)

### Environment Variables:
- `MAIL_SERVER`: SMTP server address
- `MAIL_PORT`: SMTP port (587 or 465 most common)
- `MAIL_USE_TLS`: Enable TLS encryption (true/false)
- `MAIL_USE_SSL`: Enable SSL encryption (true/false)
- `MAIL_USERNAME`: Your email address
- `MAIL_PASSWORD`: Your password or app-specific password
- `MAIL_DEFAULT_SENDER`: Default sender email address

---

## Testing Email Configuration

After updating your .env file:

1. **Restart the Flask application**
   ```bash
   python run.py
   ```

2. **Test by creating a project and adding team members**
   - The system will attempt to send welcome emails
   - Check the console logs for email status messages

3. **Check console output for errors**
   - Look for "Email sent successfully" or error messages
   - Common errors and solutions are listed below

---

## Troubleshooting

### Common Issues and Solutions:

**Gmail "Username and Password not accepted"**
- ✅ **Solution**: You're using your regular password instead of an App Password
- ✅ **Fix**: Generate and use a 16-character App Password

**Yahoo "Authentication failed"**
- ✅ **Solution**: Need to enable app passwords
- ✅ **Fix**: Enable 2-step verification and generate app password

**Outlook "Connection refused"**
- ✅ **Solution**: Check server settings and port
- ✅ **Fix**: Use `smtp-mail.outlook.com` with port 587

**"Connection refused" errors**
- ✅ **Solution**: Check MAIL_SERVER and MAIL_PORT settings
- ✅ **Fix**: Verify the SMTP server address and port for your provider

**TLS/SSL errors**
- ✅ **Solution**: Check TLS/SSL settings
- ✅ **Fix**: Use TLS for port 587, SSL for port 465

**"No emails sent" but no errors**
- ✅ **Solution**: Check that MAIL_USERNAME is configured
- ✅ **Fix**: Ensure all required environment variables are set

**Firewall/Network issues**
- ✅ **Solution**: Some networks block SMTP ports
- ✅ **Fix**: Try different ports or contact your network administrator

---

## Security Best Practices

1. **Use App Passwords**: Always use app-specific passwords when available
2. **Enable 2FA**: Enable two-factor authentication on your email account
3. **Environment Variables**: Never commit email credentials to version control
4. **Regular Updates**: Rotate passwords and app passwords regularly
5. **Monitor Usage**: Check your email provider's security logs regularly

---

## Example .env File

Create a `.env` file in your project root with your chosen provider settings:

```env
# Database
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///pi_management.db

# Email Configuration (Choose one provider)
# Gmail
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USE_SSL=false
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_DEFAULT_SENDER=your-email@gmail.com

# Yahoo (Alternative)
# MAIL_SERVER=smtp.mail.yahoo.com
# MAIL_PORT=587
# MAIL_USE_TLS=true
# MAIL_USE_SSL=false
# MAIL_USERNAME=your-email@yahoo.com
# MAIL_PASSWORD=your-app-password
# MAIL_DEFAULT_SENDER=your-email@yahoo.com

# Outlook (Alternative)
# MAIL_SERVER=smtp-mail.outlook.com
# MAIL_PORT=587
# MAIL_USE_TLS=true
# MAIL_USE_SSL=false
# MAIL_USERNAME=your-email@outlook.com
# MAIL_PASSWORD=your-password
# MAIL_DEFAULT_SENDER=your-email@outlook.com
```

---

## Need Help?

If you're still having issues:
1. Check the Flask console logs for specific error messages
2. Verify your email provider's SMTP settings
3. Test with a simple email client first
4. Contact your email provider's support if authentication fails

The system will work with any SMTP-compatible email provider - just use the correct server settings!