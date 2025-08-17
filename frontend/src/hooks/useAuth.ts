import { useEffect, useState } from "react";
import { supabase } from "../lib/supabase";

export function useAuth() {
    const [user, setUser] = useState<any>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        supabase.auth.getUser().then(({ data }) => {
        setUser(data.user ?? null);
        setLoading(false);
    });

    const { data: subscription } = supabase.auth.onAuthStateChange(
    (_event, session) => {
        setUser(session?.user ?? null);
    }
    );

    return () => {
        subscription.subscription.unsubscribe();
    };
}, []);

return { user, loading };
}
