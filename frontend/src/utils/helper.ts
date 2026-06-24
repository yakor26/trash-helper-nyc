
export interface Category {
    id: number
    col_type: string
    category_name: string
    disposal_instructions: string
    accept_special_waste_site: boolean
    accept_safe_disposal_site: boolean
    }

export interface ResultProps {
    data: Category[];
}