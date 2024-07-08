<script setup>
import { InfoFilled, Plus, Promotion } from "@element-plus/icons-vue";
import { inject, onMounted, ref } from "vue";
import { ElMessage } from "element-plus";
import { academicDiscplines } from "@/assets/static/js/resources.js";

const upload = ref();
const dialogImageUrl = ref('');
const dialogVisible = ref(false);
const handleExceed = (files) => {
  ElMessage({
    message: 'You can only upload one image at a time 😣',
    type: 'warning',
    duration: 2000
  });
};
const fileList = ref([]);
const handlePictureCardPreview = async (file) => {
  dialogImageUrl.value = file.url;
  dialogVisible.value = true;
};
const handleRemove = (file, fileList) => {
  console.log(file, fileList);
};

const courseForm = ref({});

const rules = {
  name: [
    { required: true, message: 'Please enter the course name', trigger: 'blur' },
  ],
};

const dataSource = ref([]);
let id = 1;
const append = (data) => {
  const newChild = { id: id++, label: 'New chapter', children: [] };
  if (!data.children) {
    data.children = [];
  }
  data.children.push(newChild);
  dataSource.value = [...dataSource.value];
  workObject.value = dataSource.value;
};
const edit = (data) => {
  data.label = chapterName.value;
  chapterName.value = '';
  dataSource.value = [...dataSource.value];
  workObject.value = dataSource.value;
};
const appendParent = (data) => {
  const newChild = { id: id++, label: 'New chapter', children: [] };
  dataSource.value.push(newChild);
  workObject.value = dataSource.value;
};
const remove = (node, data) => {
  const parent = node.parent;
  const children = parent.data.children || parent.data;
  const index = children.findIndex((d) => d.id === data.id);
  children.splice(index, 1);
  dataSource.value = [...dataSource.value];
  workObject.value = dataSource.value;
};

const chapterName = ref('');

const workObject = inject('workObject');
const workRule = inject('workRule');
onMounted(() => {
  workObject.value = dataSource.value;
});
</script>

<template>
  <div class="Center-Flex" style="width: 100%">
    <div class="glowing-container" style="width: 100%; max-width: 1100px">
      <el-form
          :rules="rules"
          label-width="auto"
      >
        <div class="Space-Between-Flex">
          <div class="Center-Flex" style="flex-direction: column">
            <el-text style="margin-bottom: 12px">Course Image</el-text>
            <el-upload
                v-model:file-list="fileList"
                :limit="1"
                :auto-upload="false"
                ref="upload"
                :list-type="'picture-card'"
                :on-exceed="handleExceed"
                :on-preview="handlePictureCardPreview"
                :on-remove="handleRemove"
            >
              <el-icon><Plus /></el-icon>
            </el-upload>
          </div>
          <el-divider direction="vertical" style="height: 164px; margin-left: 24px; margin-right: 24px"/>
          <div style="width: 100%">
            <div class="Space-Between-Flex">
              <el-form-item label="Course Name" props="name" required style="flex: 1">
                <el-input v-model="courseForm.name"
                          style="max-width: 280px"
                          maxlength="30"
                          show-word-limit
                          placeholder="Please enter course name"
                >
                </el-input>
              </el-form-item>
              <el-form-item label="Academic Discipline" props="name" required style="flex: 1; width: 100%">
                <el-cascader
                    v-model="courseForm.illustration"
                    :options="academicDiscplines"
                />
              </el-form-item>
            </div>
            <el-form-item label="Teaching Objectives" props="name">
              <el-input v-model="courseForm.principle"
                        maxlength="120"
                        :autosize="{ minRows: 2, maxRows: 4 }"
                        show-word-limit
                        placeholder="Please enter course teaching objectives" type="textarea"
              >
              </el-input>
            </el-form-item>
            <el-form-item label="Teaching Principles" props="name">
              <el-input v-model="courseForm.target"
                        maxlength="120"
                        :autosize="{ minRows: 2, maxRows: 4 }"
                        show-word-limit
                        placeholder="Please enter course teaching principles" type="textarea"
              >
              </el-input>
            </el-form-item>
          </div>
        </div>
        <el-divider/>
        <el-form-item label="Course Background" props="name">
          <el-input v-model="courseForm.background"
                    maxlength="120"
                    :autosize="{ minRows: 2, maxRows: 4 }"
                    show-word-limit
                    placeholder="Please enter course background" type="textarea"
          >
          </el-input>
        </el-form-item>
        <el-form-item label="Course Description" props="name">
          <el-input v-model="courseForm.description"
                    maxlength="600"
                    :autosize="{ minRows: 4, maxRows: 8 }"
                    show-word-limit
                    placeholder="Please enter course description" type="textarea"
          >
          </el-input>
        </el-form-item>
        <el-divider content-position="left" style="margin-top: 32px">
          <el-text>Chapter List
            <el-button :icon="Plus" type="primary" size="small" style="margin-left: 12px"
                       @click="appendParent(dataSource)"
            >Add</el-button>
          </el-text>
        </el-divider>
        <div style="width: 100%; height: 240px">
          <el-scrollbar>
            <el-tree
                v-if="dataSource.length"
                :data="dataSource"
                node-key="id"
                default-expand-all
                :expand-on-click-node="false"
            >
              <template #default="{ node, data }">
                <span class="custom-tree-node">
                  <span>{{ node.label }}</span>
                  <span>
                    <el-button @click="append(data)"
                               size="small"
                               style="color:var(--el-color-primary);"> Add </el-button>
                    <el-popover
                        width="220"
                        :icon="InfoFilled"
                        placement="right"
                        icon-color="#626AEF"
                        trigger="click"
                    >
                      <template #reference>
                         <el-button size="small"
                                    @click="chapterName=data.label"
                         > Edit </el-button>
                      </template>
                      <el-input size="small" v-model="chapterName" placeholder="Please enter chapter name" />
                        <div style="
                            margin-top: 12px;
                            display: flex;
                            justify-content: right;
                            align-content: flex-end">
                          <el-button type="danger"
                                     size="small"
                                     @click="chapterName=''">
                            Cancel
                          </el-button>
                           <el-button
                               @click="edit(data)"
                               :icon="Promotion" type="success" size="small">
                            Confirm
                          </el-button>
                        </div>
                    </el-popover>
  
                    <el-button  style="margin-left: 8px; color: var(--el-color-danger)"
                                size="small"
                                @click="remove(node, data)"> Delete </el-button>
                  </span>
                </span>
              </template>
            </el-tree>
            <el-empty v-else/>
          </el-scrollbar>
        </div>
        <div class="Center-Flex" style="width: 100%">
          <el-divider>
            <el-button :icon="Promotion" type="success">Create Course</el-button>
          </el-divider>
        </div>
      </el-form>
      <el-dialog v-model="dialogVisible">
        <div class="Center-Flex" style="width: 100%">
          <img w-full :src="dialogImageUrl" alt="Preview Image" />
        </div>
      </el-dialog>
    </div>
  </div>
</template>

<style scoped>
.custom-tree-node {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 14px;
  padding-right: 8px;
}
</style>
