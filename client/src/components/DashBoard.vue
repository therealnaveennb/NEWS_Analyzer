<template>
  <div class="dashboard">
    <div v-if="error" class="error">
      {{ error }}
    </div>
    <div v-else-if="loading" class="loading">
      Loading...
    </div>
    <div v-else>
      <table class="article-table">
        <thead>
          <tr>
            <th>S.No</th>
            <th>Title</th>
            <th>Author</th>
            <th>Source</th>
            <th>Published Date</th>
            <th>Feedback</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(article, index) in paginatedArticles" :key="index">
            <td>{{ index + 1 + (currentPage - 1) * itemsPerPage }}</td>
            <td>{{ article.title }}</td>
            <td>{{ article.author }}</td>
            <td>{{ article.source }}</td>
            <td>{{ formatDate(article.pub_date) }}</td> <!-- Use the formatDate method here -->
            <td>
              <span :class="['feedback-dot', feedbackClass(article.label)]"></span>
              {{ feedbackText(article.label) }}
            </td>
          </tr>
        </tbody>
      </table>
      <div class="pagination">
        <button @click="prevPage" :disabled="currentPage === 1">Previous</button>
        <span>Page {{ currentPage }} of {{ totalPages }}</span>
        <button @click="nextPage" :disabled="currentPage === totalPages">Next</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'DashBoard',
  data() {
    return {
      articles: [],
      loading: true,
      error: null,
      currentPage: 1,
      itemsPerPage: 10,
    };
  },
  computed: {
    totalPages() {
      return Math.ceil(this.articles.length / this.itemsPerPage);
    },
    paginatedArticles() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      const end = start + this.itemsPerPage;
      return this.articles.slice(start, end);
    },
  },
  mounted() {
    this.fetchArticles();
  },
  methods: {
    async fetchArticles() {
      try {
        const response = await axios.get('http://localhost:5000/articles');
        this.articles = response.data;
      } catch (err) {
        this.error = 'Failed to load articles data.';
        console.log(err);
      } finally {
        this.loading = false;
      }
    },
    nextPage() {
      if (this.currentPage < this.totalPages) {
        this.currentPage++;
      }
    },
    prevPage() {
      if (this.currentPage > 1) {
        this.currentPage--;
      }
    },
    feedbackText(label) {
      return label === -1 ? 'Negative' : label === 0 ? 'Neutral' : 'Positive';
    },
    feedbackClass(label) {
      return label === -1 ? 'negative' : label === 1 ? 'positive' : 'neutral';
    },
    formatDate(dateString) {
      const date = new Date(dateString);
      const options = {
        weekday: 'short',  // e.g., "Tue"
        day: '2-digit',    // e.g., "22"
        month: 'short',    // e.g., "Oct"
        year: 'numeric'    // e.g., "2024"
      };
      return date.toLocaleDateString('en-GB', options);  // You can change 'en-GB' if needed
    },
  },
};
</script>
<style scoped>
.dashboard {
  max-width: 1200px;
  margin: 20px auto;
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  font-family: Arial, sans-serif;
}

.loading,
.error {
  text-align: center;
  color: #555;
  font-size: 18px;
}

.article-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

.article-table th, 
.article-table td {
  border: 1px solid #ddd;
  padding: 12px 15px;
  text-align: left;
}

.article-table th {
  background-color: #4CAF50;
  color: white;
  font-weight: bold;
  text-transform: uppercase;
}

.article-table tr:nth-child(even) {
  background-color: #f2f2f2;
}

.article-table tr:hover {
  background-color: #f1f1f1;
}

.feedback-dot {
  display: inline-block;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  margin-right: 5px;
  vertical-align: middle;
}

.feedback-dot.positive {
  background-color: green;
}

.feedback-dot.negative {
  background-color: red;
}

.feedback-dot.neutral {
  background-color: grey;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 20px;
}

.pagination button {
  padding: 8px 12px;
  margin: 0 10px;
  font-size: 16px;
  cursor: pointer;
  border: none;
  border-radius: 4px;
  background-color: #4CAF50;
  color: white;
  transition: background-color 0.3s;
}

.pagination button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.pagination button:hover:not(:disabled) {
  background-color: #45a049;
}

.pagination span {
  font-size: 16px;
}
</style>
