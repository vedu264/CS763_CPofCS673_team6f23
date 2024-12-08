import React, { useState, useEffect } from 'react';
import axios from 'axios';

const Register = ({ onClose }) => {
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState({
    name: '',
    email: '',
    password: '',
  });
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState('');

  const isEduEmail = (email) => {
    return email.endsWith('.edu');
  };

  const isStrongPassword = (password) => {
    const regex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,12}$/;
    return regex.test(password);
  };

  // Session Timeout Logic
  useEffect(() => {
    const sessionTimeout = 15 * 60 * 1000; // 15 minutes
    const warningTime = 5 * 60 * 1000; // 5 minutes before timeout

    let warningTimer;
    let logoutTimer;

    const showWarning = () => {
      alert('Your session is about to expire. Please save your work!');
    };

    const handleSessionExpiration = () => {
      alert('Your session has expired. You will be logged out.');
      window.location.href = '/logout/';  // Redirect to logout page
    };

    // Reset session timers on user activity
    const resetSessionTimers = () => {
      clearTimeout(warningTimer);
      clearTimeout(logoutTimer);
      startSessionTimers();
    };

    const startSessionTimers = () => {
      warningTimer = setTimeout(showWarning, sessionTimeout - warningTime);
      logoutTimer = setTimeout(handleSessionExpiration, sessionTimeout);
    };

    // Set event listeners for activity
    window.addEventListener('mousemove', resetSessionTimers);
    window.addEventListener('keypress', resetSessionTimers);

    startSessionTimers();  // Start the session timers

    return () => {
      // Clean up timers and event listeners when the component is unmounted
      clearTimeout(warningTimer);
      clearTimeout(logoutTimer);
      window.removeEventListener('mousemove', resetSessionTimers);
      window.removeEventListener('keypress', resetSessionTimers);
    };
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    if (!data.name || !data.email || !data.password) {
      setError('Please fill all the fields');
      console.log('Error set:', error);
      return;
    }

    if (!isStrongPassword(data.password)) {
      setError('Password must be 8-12 characters long and include at least one uppercase letter, one lowercase letter, one number, and one special character.');
      return;
    }

    try {
      setLoading(true);
      const res = await axios.post('/api/users/register', data);
      if(res.status !== 200){
        throw new Error(res.data.message || 'Registration failed');
      }

      setLoading(false);
      onClose();
    } catch (error) {
      setError(error.response?.data?.message || error.message);
      setLoading(false);
    }
  };

  return (
    <div className="max-w-md mx-auto space-y-8">
      {/* Your registration form */}
    </div>
  );
};

export default Register;
