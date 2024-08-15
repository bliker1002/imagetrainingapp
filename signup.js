import React, { useState } from 'react';
import axios from 'axios';
import { loadStripe } from '@stripe/stripe-js';

const stripePromise = loadStripe('your_stripe_publishable_key_here');

export default function Signup() {
  const [formData, setFormData] = useState({
    firstName: '', lastName: '', email: '', modelName: '',
    images: null, labels: null
  });
  const [cost, setCost] = useState(null);

  const handleInputChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleFileUpload = async (e) => {
    const { name, files } = e.target;
    setFormData({ ...formData, [name]: files[0] });

    if (formData.images && formData.labels) {
      const formDataToSend = new FormData();
      formDataToSend.append('images', formData.images);
      formDataToSend.append('labels', formData.labels);

      try {
        const response = await axios.post('/api/upload', formDataToSend);
        setCost(response.data.cost);
      } catch (error) {
        console.error('Error uploading files:', error);
      }
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const stripe = await stripePromise;

    try {
      const response = await axios.post('/api/signup', formData);
      const { session_id } = response.data;

      const result = await stripe.redirectToCheckout({
        sessionId: session_id,
      });

      if (result.error) {
        console.error(result.error.message);
      }
    } catch (error) {
      console.error('Error during signup:', error);
    }
  };

  return (
    <div className="container mt-5">
      <h2 className="mb-4">Sign Up for AI Image Model Maker</h2>
      <form onSubmit={handleSubmit}>
        <div className="mb-3">
          <input type="text" className="form-control" name="firstName" onChange={handleInputChange} placeholder="First Name" required />
        </div>
        <div className="mb-3">
          <input type="text" className="form-control" name="lastName" onChange={handleInputChange} placeholder="Last Name" required />
        </div>
        <div className="mb-3">
          <input type="email" className="form-control" name="email" onChange={handleInputChange} placeholder="Email" required />
        </div>
        <div className="mb-3">
          <input type="text" className="form-control" name="modelName" onChange={handleInputChange} placeholder="Model Name" required />
        </div>
        <div className="mb-3">
          <label className="form-label">Upload Images (Folder)</label>
          <input type="file" className="form-control" name="images" onChange={handleFileUpload} webkitdirectory="" directory="" multiple required />
        </div>
        <div className="mb-3">
          <label className="form-label">Upload Labels (JSON)</label>
          <input type="file" className="form-control" name="labels" accept=".json" onChange={handleFileUpload} required />
        </div>
        {cost && <p className="alert alert-info">Estimated cost: ${cost}</p>}
        <button type="submit" className="btn btn-primary" disabled={!cost}>Sign Up and Pay</button>
      </form>
    </div>
  );
}