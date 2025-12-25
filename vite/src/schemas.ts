export interface carSchema {
        _id: string,
        owner:string,
        brand:string,
        model:string,
        image: string,
        year: number,
        category:string,
        seating_capacity: number,
        fuel_type:string,
        transmission:string,
        pricePerDay: number,
        location:string,
        description:string,
        isAvaliable:boolean,
        createdAt: string
    }

export interface bookingSChema{
            _id:string,
            car: carSchema,
            user:string,
            owner:string,
            pickupDate:string,
            returnDate:string,
            status:string,
            price:number,
            createdAt:string,
}