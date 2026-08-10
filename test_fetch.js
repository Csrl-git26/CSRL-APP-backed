async function run() {
  const loginRes = await fetch('https://csrl-app-backed-1.onrender.com/api/auth/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ rollKey: '2601001', pin: '0000' }) // Wait, do I know a valid PIN? If it's an admin?
  });
  console.log(loginRes.status);
}
run();
