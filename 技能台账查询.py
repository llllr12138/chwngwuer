import streamlit as st
import pandas as pd
from pathlib import Path
import hashlib
from abc import ABC, abstractmethod

class BasePage(ABC):
    """基础页面类"""
    
    def __init__(self, data_file, sheet_name, title):
        self.data_file = data_file
        self.sheet_name = sheet_name
        self.title = title
    
    def read_data(self):
        """读取Excel数据的通用方法"""
        if not Path(self.data_file).exists():
            return None, None, None
        
        try:
            df = pd.read_excel(self.data_file, sheet_name=self.sheet_name)
            # 第2列是姓名，第3列开始是项目
            name_col = df.columns[1]
            skill_cols = df.columns[2:]
            df_result = df[[name_col] + list(skill_cols)].dropna(subset=[name_col])
            return df_result, name_col, skill_cols
        except Exception as e:
            st.error(f"读取数据时出错: {str(e)}")
            return None, None, None
    
    @abstractmethod
    def render(self):
        """渲染页面内容，子类必须实现"""
        pass

class SkillQueryPage(BasePage):
    """关键技能查询页面"""
    
    def __init__(self):
        super().__init__("skill_data.xlsx", "26年度关键技能数据", "关键技能查询")
    
    def render(self):
        st.subheader("关键技能查询")
        
        if not Path(self.data_file).exists():
            st.warning("请先上传关键技能Excel文件")
            return
        
        df, name_col, cols = self.read_data()
        if df is None:
            return
        
        # 查询界面
        col1, col2 = st.columns([3, 1])
        
        with col1:
            names = sorted(df[name_col].astype(str).str.strip())
            search = st.selectbox("选择姓名", [""] + names, 
                                format_func=lambda x: "请选择..." if x == "" else x,
                                key="skill_select")
        
        with col2:
            query_btn = st.button("查询技能", use_container_width=True)
        
        if query_btn:
            if search == "":
                st.warning("请选择一个姓名")
            else:
                try:
                    row = df[df[name_col].astype(str).str.strip() == search].iloc[0]
                    
                    # 准备显示数据，只显示空值数据，显示为"未完成"
                    data = []
                    for col in cols:
                        value = row[col]
                        if pd.isna(value):  # 只处理空值
                            data.append({
                                "项目名称": col,
                                "数据内容": "未完成"
                            })
                        else:
                            display_value = str(value).strip()
                            # 如果值是"无数据"、"否"等也视为未完成
                            if display_value.lower() in ["无数据", "否", "null", "none", "-", ""]:
                                data.append({
                                    "项目名称": col,
                                    "数据内容": "未完成"
                                })
                    
                    st.success(f"关键技能查询结果：{search}")
                    
                    if len(data) > 0:
                        result_df = pd.DataFrame(data)
                        st.dataframe(
                            result_df, 
                            use_container_width=True, 
                            height=min(600, len(data) * 40 + 100)
                        )
                        st.info(f"共显示 {len(data)} 个未完成项目")
                    else:
                        st.info("所有技能项目已完成")
                        
                except IndexError:
                    st.error("未找到该人员技能信息")
                except Exception as e:
                    st.error(f"技能查询出错: {str(e)}")

class JobQueryPage(BasePage):
    """关键作业查询页面"""
    
    def __init__(self):
        super().__init__("job_data.xlsx", "26年度关键技能数据", "关键作业查询")
    
    def render(self):
        st.subheader("关键作业查询")
        
        if not Path(self.data_file).exists():
            st.warning("请先上传关键作业Excel文件")
            return
        
        df, name_col, cols = self.read_data()
        if df is None:
            return
        
        # 查询界面
        col1, col2 = st.columns([3, 1])
        
        with col1:
            names = sorted(df[name_col].astype(str).str.strip())
            search = st.selectbox("选择姓名", [""] + names, 
                                format_func=lambda x: "请选择..." if x == "" else x,
                                key="job_select")
        
        with col2:
            query_btn = st.button("查询作业", use_container_width=True)
        
        if query_btn:
            if search == "":
                st.warning("请选择一个姓名")
            else:
                try:
                    row = df[df[name_col].astype(str).str.strip() == search].iloc[0]
                    
                    # 准备显示数据，只显示空值数据，显示为"未完成"
                    data = []
                    for col in cols:
                        value = row[col]
                        if pd.isna(value):  # 只处理空值
                            data.append({
                                "项目名称": col,
                                "数据内容": "未完成"
                            })
                        else:
                            display_value = str(value).strip()
                            # 如果值是"无数据"、"否"等也视为未完成
                            if display_value.lower() in ["无数据", "否", "null", "none", "-", ""]:
                                data.append({
                                    "项目名称": col,
                                    "数据内容": "未完成"
                                })
                    
                    st.success(f"关键作业查询结果：{search}")
                    
                    if len(data) > 0:
                        result_df = pd.DataFrame(data)
                        st.dataframe(
                            result_df, 
                            use_container_width=True, 
                            height=min(600, len(data) * 40 + 100)
                        )
                        st.info(f"共显示 {len(data)} 个未完成项目")
                    else:
                        st.info("所有作业项目已完成")
                        
                except IndexError:
                    st.error("未找到该人员作业信息")
                except Exception as e:
                    st.error(f"作业查询出错: {str(e)}")

class NewFeaturePage(BasePage):
    """新功能页面模板 - 可以快速添加新功能"""
    
    def __init__(self):
        super().__init__("new_feature_data.xlsx", "26年度新功能数据", "新功能查询")
    
    def render(self):
        st.subheader("新功能查询")
        st.info("这是一个新功能的示例，可以基于BasePage快速创建新功能")

class AppManager:
    """应用管理器"""
    
    def __init__(self):
        # 定义所有页面
        self.pages = {
            "关键技能查询": SkillQueryPage(),
            "关键作业查询": JobQueryPage(),
            "新功能示例": NewFeaturePage(),  # 示例，可以随时替换
        }
        
        # 初始化session state
        if 'authenticated' not in st.session_state:
            st.session_state.authenticated = False
        if 'current_page' not in st.session_state:
            st.session_state.current_page = "关键技能查询"
        
        self.password = “cw100141”  # 管理员密码
    
    def hash_password(self, password):
        """密码哈希"""
        return hashlib.md5(password.encode()).hexdigest()
    
    def verify_password(self, input_password):
        """验证密码"""
        return self.hash_password(input_password) == self.hash_password(self.password)
    
    def login_page(self):
        """登录页面"""
登录标题("登录")
        password_input = st.text_input("请输入管理员密码", type="password")
        
        if st.button("登录"):
如果self。验证密码(密码输入):
st.会话状态.已认证 = True
st.成功(“登录成功！”)
                st.rerun()
            else:
                st.error("密码错误！")
        st.stop()
    
    def sidebar_menu(self):
        """侧边栏菜单"""
        with st.sidebar:
            st.header("管理上传")
            
            # 根据当前页面显示对应的上传控件
            current_page_obj = self.pages[st.session_state.current_page]
            
            if isinstance(current_page_obj, SkillQueryPage):
                f = st.file_uploader("上传关键技能Excel", type=["xlsx", "xls"], key="skill_upload")
                if f:
                    with open(current_page_obj.data_file, "wb") as fw:
                        fw.write(f.getbuffer())
                    st.success("关键技能数据上传成功")
                    st.rerun()st.重新运行()
            elif isinstance(current_page_obj, JobQueryPage):
                f = st.file_uploader("上传关键作业Excel", type=["xlsx", "xls"], key="job_upload")
                if f:
                    with open(current_page_obj.data_file, "wb") as fw:
                        fw.write(f.getbuffer())
                    st.success("关键作业数据上传成功")
                    st.rerun()st.重新运行()st.重新运行()st.重新运行()
            else:
                # 其他页面的上传控件
                st.info(f"当前页面: {st.session_state.current_page}")
            
            # 一级菜单 - 页面选择
            st.divider()st.分隔符()圣。分隔符()
            st.subheader副标题副标题副标题副标题副标题副标题副标题副标题副标题副标题副标题副标题副标题副标题副标题副标题("功能导航")圣。subheader圣。子标题圣。子标题圣。子标题圣。子标题圣。子标题圣。子标题圣。子标题圣。子标题圣。子标题圣。子标题圣。子标题圣。子标题圣。子标题圣。子标题("功能导航")st.子标题(圣。子标题(圣。子标题(圣。子标题(“功能导航”)
            
            for page_name in self.pages.keys():
                (如果按钮(如果按钮(如果按钮如果按钮(如果按钮
                    page_name, 页面名称,
                    use_container_width=True,使用容器宽度=True,
                    type="secondary" if st.session_state.current_page != page_name else "primary"
                ):
                    st.session_state.current_page = page_namest.session_state.current_page= page_name
                    st.rerun()st.重新运行()st.重新运行()st.重新运行()st.重新运行()st.重新运行()st.重新运行()st.重新运行()st.重新运行()圣。重新运行()st.重新运行()圣。重新运行()st.重新运行()圣。重新运行()st.重新运行()圣。重新运行()st.重新运行()圣。重新运行()st.重新运行()圣。重新运行()st.重新运行()圣。重新运行()st.重新运行()圣。重新运行()
            
            # 退出登录
            if st.button("退出登录", use_container_width=True):
                st.session_state.authenticated = False
                st.rerun()st.重新运行()st.重新运行()st.重新运行()st.重新运行()st.重新运行()st.重新运行()st.重新运行()st.重新运行()st.重新运行()st.重新运行()st.重新运行()圣。重新运行()st.重新运行()圣。重新运行()st.重新运行()圣。重新运行()st.重新运行()圣。重新运行()st.重新运行()圣。重新运行()st.重新运行()圣。重新运行()st.重新运行()圣。重新运行()st.重新运行()圣。重新运行()st.重新运行()圣。重新运行()st.重新运行()圣。重新运行()st.重新运行()圣。重新运行()
    
    def main_content(self):
        """主内容区域"""
        current_page = st.session_state.current_page
        page_obj = self.pages[current_page]
        
        # 渲染当前页面
        page_obj.render()页面对象.渲染()
        
        # 数据概览
        st.divider()st.分隔符()st.分隔符()圣。分隔符()圣。分隔符()圣。分隔符()
圣。子标题(“数据概览”)
        
        df, name_col, cols = page_obj.read_data()
        if df is not None:
            col1, col2 = st.columns(2)
与列1：与列1：列1：与列1：列1：与列1：列1：与列1：
{圣。写圣。写圣。写圣。写f"**{圣。写写圣。写写(f"**{圣。write圣。写圣。写圣。写(f"**{page_obj.title标题标题标题标题标题标题标题标题标题标题}**")
圣。写(f"- 总人数:{len(df)}")
圣。写(f"- 项目数: {len(cols)}")
            with col2:与列2:与列2:与列2:与列2:与列2:
                st.write(f"- 姓名列: {name_col}")
                if len(列) > 0:如果 长度(列) > 0:如果 长度(列) > 0:如果长度(列) > 0:如果 长度(列) > 0:如果 长度(列) > 0:如果长度(列) > 0:如果 长度(列) > 0:如果 长度(列) > 0:如果长度(列) > 0:如果 长度(列) > 0:如果 长度(列) > 0:如果长度(列) > 0:
                    st.write(f"- 首个项目: {cols[0]}")
        else:否则:否则:
st.warning(“当前功能数据未上传: st.warning(“当前功能数据未上传: st.warning(“当前功能数据未上传: st.warning(“当前功能数据未上传: st.warning(“当前功能数据未上传: st.warning(“当前功能数据未上传: st.warning(“当前功能数据未上传: st.warning(“当前功能数据未上传: st.warning(“当前功能数据未上传: st.warning(“当前功能数据未上传: st.warning(“当前功能数据未上传:{page_obj.title}")
    
    def run(self):
        """运行应用"""
        # 设置页面配置
        st.set_page_config(
            page_title="技能作业查询系统", 
            page_icon="📋", 
            layout="wide",布局="宽",
initial_sidebar_state=“expanded”
        )
        
st.title(“技能作业查询系统”)
        
        # 验证登录状态
        if not st.session_state.authenticated:
            self.login_page()
        
        # 显示侧边栏和主内容
        self.sidebar_menu()
        self.main_content()

# 运行应用
如果__name__ =="__main__":
    app = AppManager()
应用。运行()
