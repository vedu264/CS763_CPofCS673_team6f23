import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const Login = ({ onClose }) => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [data, setData] = useState({
    email: '',
    password: '',
  });
  const [showPassword, setShowPassword] = useState(false);

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
    if (!data.email || !data.password) {
      setError('Please fill in all fields');
      return;
    }
    try {
      setLoading(true);
      const res = await axios.post('/api/users/login', data);
      if (res.status !== 200) {
        throw new Error('Login failed');
      }
      const resData = res.data;
      setLoading(false);
      localStorage.setItem('token', resData.token);
      localStorage.setItem('user', JSON.stringify(resData.user));
      onClose();
      navigate('/marketplace');
    } catch (error) {
      setError(error.response?.data?.message || 'Login failed');
      setLoading(false);
    }
  };

  return (
    <div className="max-w-md mx-auto">
      {/* Your login form */}
    </div>
  );
};

export default Login;
