import { ref, provide, inject } from 'vue';

const AUTH_KEY = Symbol('auth');

export function provideAuth() {
    const loading = ref(false);
    const error = ref(null);
    const user = ref(null);

    const setLoading = (value) => {
        loading.value = value;
    };

    const setError = (value) => {
        error.value = value;
    };

    const setUser = (value) => {
        user.value = value;
    };

    const auth = {
        loading,
        error,
        user,
        setLoading,
        setError,
        setUser
    };

    provide(AUTH_KEY, auth);

    return auth;
}

export function useAuth() {
    const auth = inject(AUTH_KEY);
    if (!auth) {
        throw new Error('useAuth must be used within a component that has called provideAuth');
    }
    return auth;
} 