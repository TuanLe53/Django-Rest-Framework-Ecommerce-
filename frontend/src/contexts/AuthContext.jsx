import { createContext, useState, useEffect } from "react";
import {jwtDecode} from "jwt-decode";
import { useNavigate } from "react-router-dom";
import URL from "../api/urls";

const AuthContext = createContext();
export default AuthContext;

export const AuthProvider = ({ children }) => {
    let [authToken, setAuthTokens] = useState(() => localStorage.getItem("authToken") ? JSON.parse(localStorage.getItem("authToken")) : null);
    let [user, setUser] = useState(() => localStorage.getItem("authToken") ? jwtDecode(localStorage.getItem("authToken")) : null);
    let [isLogin, setIsLogin] = useState(() => localStorage.getItem("authToken") ? true : false);
    let [loading, setLoading] = useState(true);

    const navigate = useNavigate();

    const handleLogin = async (form) => {
        let res = await fetch(URL.Auth + "login/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                "email": form.email,
                "password": form.password
            })
        })

        let data = await res.json()
        if (res.status === 200) {
            setAuthTokens(data)
            setUser(jwtDecode(data.access))
            localStorage.setItem("authToken", JSON.stringify(data))
            setIsLogin(true)
            navigate("/")
        } else {
            alert(data.detail)
        }
    }

    let handleLogout = () => {
        setAuthTokens(null)
        setUser(null)
        setIsLogin(null)
        localStorage.removeItem("authToken")
        navigate("/")
    }

    let updateToken = async () => {
        let res = await fetch(URL.Auth + "refresh/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body:JSON.stringify({"refresh": authToken?.refresh})
        })

        let data = await res.json()

        if (res.status === 200) {
            setAuthTokens(data)
            setUser(jwtDecode(data.access))
            localStorage.setItem("authToken", JSON.stringify(data))
        } else {
            handleLogout()
        }

        if (loading) {
            setLoading(false)
        }
    }

    let contextData = {
        user: user,
        authToken: authToken,
        isLogin: isLogin,
        handleLogin: handleLogin,
        handleLogout: handleLogout
    }

    useEffect(()=> {

        if(loading){
            updateToken()
        }

        let fourMinutes = 1000 * 60 * 4

        let interval =  setInterval(()=> {
            if(authToken){
                updateToken()
            }
        }, fourMinutes)
        return ()=> clearInterval(interval)

    }, [authToken, loading])

    return (
        <AuthContext.Provider value={contextData}>
            {loading ? null : children}
        </AuthContext.Provider>
    )
}