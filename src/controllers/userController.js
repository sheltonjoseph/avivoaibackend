const db = require('../config/db');

exports.getAllUsers = async (req, res) => {
  try {
    const [rows] = await db.promise().execute('SELECT * FROM users');
    res.json(rows);
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Database query failed' });
  }
};
