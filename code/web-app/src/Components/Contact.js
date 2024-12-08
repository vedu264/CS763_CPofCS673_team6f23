import React, { useState } from 'react';
import { sanitizeInput } from '../utils/sanitize';  // Import sanitize function

const Contact = () => {
  const [email, setEmail] = useState('');
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Sanitize the inputs before sending to the backend
    const sanitizedMessage = sanitizeInput(message);
    const sanitizedEmail = sanitizeInput(email);

    if (!sanitizedEmail || !sanitizedMessage) {
      setError('Please fill in all fields');
      return;
    }

    try {
      // Send sanitized data to the backend (assuming the API endpoint exists)
      const res = await axios.post('/api/contact', {
        email: sanitizedEmail,
        message: sanitizedMessage
      });
      // Handle success (e.g., show success message, reset form)
    } catch (error) {
      setError('Failed to submit message');
    }
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <input 
          type="email" 
          value={email} 
          onChange={(e) => setEmail(e.target.value)} 
          placeholder="Enter your email"
        />
        <textarea 
          value={message} 
          onChange={(e) => setMessage(e.target.value)} 
          placeholder="Enter your message"
        />
        <button type="submit">Submit</button>
      </form>
      {error && <p>{error}</p>}
    </div>
  );
};

export default Contact;
