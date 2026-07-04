
export type ItemCategory = {
    id: number;
    col_type: string;
    category_name: string;
    disposal_instructions: string;
    accept_special_waste_site: boolean;
    accept_safe_disposal_site: boolean;
}

export interface ResultProps {
    data: ItemCategory[];
}

export type Login = {
    username: string;
    password: string;
}

export type Register = {
    username: string;
    email: string;
    phone_number: string;
    allow_notifications: boolean;
    password: string;
    confirm_password: string;
}

export type User = {
    username: string;
    email: string;
    phone_number: string;
    allow_notifications: boolean;
    addresses: string[];
}

export interface AuthProviderProps {
    user: User | null;
    token: string;
    login: (data: Login) => void;
    logout: () => void;

}