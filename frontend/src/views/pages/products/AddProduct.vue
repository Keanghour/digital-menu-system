<template>
    <div class="add-product-container">
        <h3 class="text-center mb-4">Add New Product</h3>
        <form @submit.prevent="saveProduct">
            <div class="flex flex-col gap-6">
                <img
                    v-if="product.image"
                    :src="product.image"
                    alt="Product Image"
                    class="block m-auto pb-4"
                    style="width: 100px; height: 100px; object-fit: cover;"
                />

                <div class="flex items-center gap-4">
                    <div class="flex-1">
                        <label for="productCode" class="block font-bold mb-3">Product Code</label>
                        <div class="flex gap-4">
                            <InputText
                                id="productCode"
                                v-model.trim="product.code"
                                placeholder="Enter code manually"
                                fluid
                            />
                            <Button label="Generate" icon="pi pi-refresh" @click="generateProductCode" />
                        </div>
                    </div>
                </div>

                <div class="flex items-center gap-4">
                    <div class="flex-1">
                        <label for="name" class="block font-bold mb-3">Name</label>
                        <InputText
                            id="name"
                            v-model.trim="product.name"
                            required
                            autofocus
                            :invalid="submitted && !product.name"
                            fluid
                        />
                        <small v-if="submitted && !product.name" class="text-red-500">Name is required.</small>
                    </div>

                    <div class="flex-1">
                        <label for="imageUpload" class="block font-bold mb-3">Upload Image</label>
                        <input
                            type="file"
                            id="imageUpload"
                            accept="image/*"
                            @change="onImageUpload"
                            class="block w-full"
                        />
                    </div>
                </div>

                <div>
                    <label for="description" class="block font-bold mb-3">Description</label>
                    <Textarea
                        id="description"
                        v-model="product.description"
                        rows="3"
                        fluid
                    />
                </div>

                <div>
                    <label for="brand" class="block font-bold mb-3">Brand Name</label>
                    <InputText
                        id="brand"
                        v-model.trim="product.brand"
                        placeholder="Enter brand name"
                        fluid
                    />
                </div>

                <div>
                    <label for="inventoryStatus" class="block font-bold mb-3">Inventory Status</label>
                    <Select
                        id="inventoryStatus"
                        v-model="product.inventoryStatus"
                        :options="statuses"
                        optionLabel="label"
                        placeholder="Select a Status"
                        fluid
                    />
                </div>

                <div>
                    <span class="block font-bold mb-4">Category</span>
                    <div class="grid grid-cols-12 gap-4">
                        <div class="flex items-center gap-2 col-span-6">
                            <RadioButton id="category1" v-model="product.category" name="category" value="Accessories" />
                            <label for="category1">Accessories</label>
                        </div>
                        <div class="flex items-center gap-2 col-span-6">
                            <RadioButton id="category2" v-model="product.category" name="category" value="Clothing" />
                            <label for="category2">Clothing</label>
                        </div>
                        <div class="flex items-center gap-2 col-span-6">
                            <RadioButton id="category3" v-model="product.category" name="category" value="Electronics" />
                            <label for="category3">Electronics</label>
                        </div>
                        <div class="flex items-center gap-2 col-span-6">
                            <RadioButton id="category4" v-model="product.category" name="category" value="Fitness" />
                            <label for="category4">Fitness</label>
                        </div>
                    </div>
                </div>

                <div class="grid grid-cols-12 gap-4">
                    <div class="col-span-6">
                        <label for="price" class="block font-bold mb-3">Price</label>
                        <InputNumber
                            id="price"
                            v-model="product.price"
                            mode="currency"
                            currency="USD"
                            locale="en-US"
                            fluid
                        />
                    </div>
                    <div class="col-span-6">
                        <label for="quantity" class="block font-bold mb-3">Quantity</label>
                        <InputNumber
                            id="quantity"
                            v-model="product.quantity"
                            integeronly
                            fluid
                        />
                    </div>
                </div>
            </div>

            <div class="flex justify-end mt-4">
                <Button label="Cancel" icon="pi pi-times" text @click="cancel" />
                <Button label="Save" icon="pi pi-check" type="submit" @click="submitted = true" />
            </div>
        </form>
    </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router'; // Import useRouter
import InputText from 'primevue/inputtext';
import InputNumber from 'primevue/inputnumber';
import Button from 'primevue/button';
import Select from 'primevue/selectbutton';
import Textarea from 'primevue/textarea';
import RadioButton from 'primevue/radiobutton';

const product = ref({
    code: '',
    name: '',
    description: '',
    brand: '',
    category: null,
    price: null,
    quantity: null,
    inventoryStatus: null,
    image: null
});

const statuses = ref([
    { label: 'In Stock', value: 'instock' },
    { label: 'Out of Stock', value: 'outofstock' }
]);

const submitted = ref(false);
const router = useRouter(); // Initialize router

function saveProduct() {
    if (product.value.name) {
        console.log('Product saved:', product.value);
        // Optionally, navigate or show a success message
    }
}

function cancel() {
    router.push({
        path: 'product',
        name: 'product',
        component: () => import('@/views/pages/products/Product.vue')
    }); // Navigate to the product route
}

function generateProductCode() {
    product.value.code = `CODE-${Math.random().toString(36).substr(2, 9).toUpperCase()}`;
}

function onImageUpload(event) {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
            const img = new Image();
            img.src = e.target.result;
            img.onload = () => {
                const canvas = document.createElement('canvas');
                const ctx = canvas.getContext('2d');

                // Resize canvas to 100x100
                canvas.width = 100;
                canvas.height = 100;
                ctx.drawImage(img, 0, 0, 100, 100);

                // Convert to data URL with 85% quality
                product.value.image = canvas.toDataURL('image/jpeg', 0.85);
            };
        };
        reader.readAsDataURL(file);
    }
}
</script>


<style scoped>
.add-product-container {
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}
.text-center {
    text-align: center;
}
</style>
