// services/auth.js
import jwt from 'jsonwebtoken';

const secret = 'your-secret-key';

export const generateToken = (user) => {
  return jwt.sign(user, secret);
};


