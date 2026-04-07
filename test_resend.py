import urllib.request, json

payload = {
    "from": "Treehouse Events <events@tigertracks.ai>",
    "to": ["events@tigertracks.ai"],
    "reply_to": "test.sponsor@example.com",
    "subject": "TEST: Sponsor Form — Resend backend verified",
    "html": """
    <div style="font-family:sans-serif;max-width:600px;margin:0 auto;padding:32px;background:#f9f9f7;border-radius:8px;">
      <h2 style="font-family:Georgia,serif;color:#1a3a1a;margin-bottom:24px;">New Sponsorship Inquiry</h2>
      <table style="width:100%;border-collapse:collapse;">
        <tr>
          <td style="padding:10px 0;border-bottom:1px solid #e0ddd6;color:#666;font-size:13px;width:140px;">Name</td>
          <td style="padding:10px 0;border-bottom:1px solid #e0ddd6;color:#1a1a1a;font-size:14px;font-weight:600;">Test Sender</td>
        </tr>
        <tr>
          <td style="padding:10px 0;border-bottom:1px solid #e0ddd6;color:#666;font-size:13px;">Brand / Company</td>
          <td style="padding:10px 0;border-bottom:1px solid #e0ddd6;color:#1a1a1a;font-size:14px;font-weight:600;">Acme Spirits Co.</td>
        </tr>
        <tr>
          <td style="padding:10px 0;border-bottom:1px solid #e0ddd6;color:#666;font-size:13px;">Email</td>
          <td style="padding:10px 0;border-bottom:1px solid #e0ddd6;color:#1a1a1a;font-size:14px;">test.sponsor@example.com</td>
        </tr>
        <tr>
          <td style="padding:10px 0;border-bottom:1px solid #e0ddd6;color:#666;font-size:13px;">Tier Interest</td>
          <td style="padding:10px 0;border-bottom:1px solid #e0ddd6;color:#1a1a1a;font-size:14px;">Gold - $10,000 / event</td>
        </tr>
        <tr>
          <td style="padding:10px 0;color:#666;font-size:13px;vertical-align:top;">Message</td>
          <td style="padding:10px 0;color:#1a1a1a;font-size:14px;line-height:1.6;">This is a test submission confirming the Resend backend is wired correctly. The form is live.</td>
        </tr>
      </table>
      <p style="margin-top:32px;font-size:12px;color:#999;">Sent via treehouseevents.cliffeliz.ai/sponsor.html</p>
    </div>
    """
}

req = urllib.request.Request(
    "https://api.resend.com/emails",
    data=json.dumps(payload).encode(),
    headers={
        "Authorization": "Bearer re_KW6i8VbG_9yepaibq73Gaeu7ysDw7guHT",
        "Content-Type": "application/json"
    },
    method="POST"
)

try:
    with urllib.request.urlopen(req) as resp:
        result = json.loads(resp.read())
        print("SUCCESS:", json.dumps(result, indent=2))
except urllib.error.HTTPError as e:
    body = e.read()
    print("ERROR:", e.code, body.decode() if body else '(empty)')
