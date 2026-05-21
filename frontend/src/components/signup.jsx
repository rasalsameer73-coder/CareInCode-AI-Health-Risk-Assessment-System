import { motion } from "framer-motion";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { register } from "../services/api";

export default function Signup() {
  const navigate = useNavigate();

  const [form, setForm] = useState({
    name: "",
    email: "",
    password: "",
    confirm: "",
    age: "",
    gender: ""
  });

  const [errors, setErrors] = useState({});

  // ✅ FIXED HANDLE CHANGE
  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm({ ...form, [name]: value });
  };

  const validate = () => {
    let err = {};

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(form.email)) err.email = "Invalid email";

    if (form.password.length < 8) err.password = "Min 8 characters";
    if (form.password !== form.confirm) err.confirm = "Passwords mismatch";
    if (!form.age) err.age = "Enter age";
    if (!form.gender) err.gender = "Select gender";

    return err;
  };

  const handleSubmit = async () => {
    const e = validate();

    if (Object.keys(e).length) {
      setErrors(e);
      return;
    }

    try {
      const result = await register({ email: form.email, password: form.password });
      if (result.success) {
        navigate("/dashboard");
      }
    } catch (err) {
      setErrors({ form: err.message || "Signup failed" });
    }
  };

  return (
    <div className="login-page">
      <motion.div
        className="login-card"
        initial={{ opacity: 0, y: 40 }}
        animate={{ opacity: 1, y: 0 }}
      >
        <h2>Create Account</h2>
        <p className="login-sub">Start your journey</p>

        <div className="login-grid">

          <div>
            <input
              name="name"
              placeholder="Name"
              onChange={handleChange}
            />
          </div>

          <div>
            <input
              name="email"
              placeholder="Email"
              onChange={handleChange}
              className={errors.email ? "input-error" : ""}
            />
            {errors.email && <span className="error">{errors.email}</span>}
          </div>

          <div>
            <input
              name="password"
              type="password"
              placeholder="Password"
              onChange={handleChange}
              className={errors.password ? "input-error" : ""}
            />
            {errors.password && <span className="error">{errors.password}</span>}
          </div>

          <div>
            <input
              name="confirm"
              type="password"
              placeholder="Confirm Password"
              onChange={handleChange}
              className={errors.confirm ? "input-error" : ""}
            />
            {errors.confirm && <span className="error">{errors.confirm}</span>}
          </div>

          <div>
            <input
              name="age"
              placeholder="Age"
              onChange={handleChange}
              className={errors.age ? "input-error" : ""}
            />
            {errors.age && <span className="error">{errors.age}</span>}
          </div>

          <div>
            <select
              name="gender"
              onChange={handleChange}
              className={errors.gender ? "input-error" : ""}
            >
              <option value="">Gender</option>
              <option>Male</option>
              <option>Female</option>
              <option>Other</option>
            </select>
            {errors.gender && <span className="error">{errors.gender}</span>}
          </div>

        </div>

        <button className="btn-primary login-btn" onClick={handleSubmit}>
          Get Started
        </button>
        {errors.form && <p className="error">{errors.form}</p>}
      </motion.div>
    </div>
  );
}